import os
import math
import json
import joblib
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from sklearn.ensemble import RandomForestRegressor

from backend.app.core.config import settings
from backend.app.core.logging import logger

FEATURE_NAMES = [
    # Room Geometry
    "room_type_bed", "room_type_living", "room_type_dining", "room_type_office", "room_type_other",
    "room_width", "room_length", "room_area", "room_aspect_ratio",
    # Furniture Properties
    "furn_cat_sofa", "furn_cat_bed", "furn_cat_table", "furn_cat_chair", "furn_cat_storage", "furn_cat_decor",
    "furn_width", "furn_height", "furn_depth", "furn_footprint", "furn_price",
    # Candidate Spatial Position
    "norm_x", "norm_z", "rot_sin", "rot_cos",
    "dist_to_center", "dist_to_min_wall", "dist_to_back_wall",
    "wall_alignment_score", "clearance_to_nearest_m"
]

class BoundingBox2D:
    def __init__(self, x: float, z: float, width: float, depth: float, rotation: float = 0.0):
        self.x = float(x)
        self.z = float(z)
        self.width = float(width)
        self.depth = float(depth)
        self.rotation = float(rotation)
        
        cos_r = abs(math.cos(rotation))
        sin_r = abs(math.sin(rotation))
        self.eff_width = (width * cos_r + depth * sin_r)
        self.eff_depth = (width * sin_r + depth * cos_r)
        
    @property
    def min_x(self) -> float:
        return self.x - self.eff_width / 2.0

    @property
    def max_x(self) -> float:
        return self.x + self.eff_width / 2.0

    @property
    def min_z(self) -> float:
        return self.z - self.eff_depth / 2.0

    @property
    def max_z(self) -> float:
        return self.z + self.eff_depth / 2.0

    def intersects(self, other: "BoundingBox2D", margin: float = 0.05) -> bool:
        return not (
            self.max_x + margin < other.min_x or
            self.min_x - margin > other.max_x or
            self.max_z + margin < other.min_z or
            self.min_z - margin > other.max_z
        )

    def is_inside_room(self, room_w: float, room_l: float, buffer: float = 0.02) -> bool:
        half_w = room_w / 2.0 - buffer
        half_l = room_l / 2.0 - buffer
        return (
            self.min_x >= -half_w and
            self.max_x <= half_w and
            self.min_z >= -half_l and
            self.max_z <= half_l
        )

    def min_distance_to(self, other: "BoundingBox2D") -> float:
        dx = max(0.0, max(self.min_x - other.max_x, other.min_x - self.max_x))
        dz = max(0.0, max(self.min_z - other.max_z, other.min_z - self.max_z))
        return math.sqrt(dx * dx + dz * dz)

class LayoutFeatureExtractor:
    """Transforms raw spatial placement candidates into normalized numeric feature vectors."""

    @staticmethod
    def extract_features(
        room_w: float,
        room_l: float,
        room_type: str,
        item_category: str,
        item_w: float,
        item_h: float,
        item_d: float,
        item_price: float,
        cand_x: float,
        cand_z: float,
        cand_rot: float,
        placed_boxes: List[BoundingBox2D]
    ) -> np.ndarray:
        half_w = max(1.0, room_w / 2.0)
        half_l = max(1.0, room_l / 2.0)
        room_area = room_w * room_l
        aspect_ratio = room_w / max(0.1, room_l)
        
        rt = room_type.lower()
        rt_bed = 1.0 if "bed" in rt else 0.0
        rt_living = 1.0 if "living" in rt else 0.0
        rt_dining = 1.0 if "dining" in rt else 0.0
        rt_office = 1.0 if "office" in rt else 0.0
        rt_other = 1.0 if (rt_bed == 0 and rt_living == 0 and rt_dining == 0 and rt_office == 0) else 0.0
        
        cat = item_category.lower()
        cat_sofa = 1.0 if ("sofa" in cat or "armchair" in cat) else 0.0
        cat_bed = 1.0 if "bed" in cat else 0.0
        cat_table = 1.0 if ("table" in cat or "desk" in cat) else 0.0
        cat_chair = 1.0 if "chair" in cat and "armchair" not in cat else 0.0
        cat_storage = 1.0 if ("wardrobe" in cat or "bookshelf" in cat or "tv" in cat) else 0.0
        cat_decor = 1.0 if ("rug" in cat or "plant" in cat or "lamp" in cat) else 0.0
        
        furn_footprint = item_w * item_d
        norm_x = cand_x / half_w
        norm_z = cand_z / half_l
        rot_sin = math.sin(cand_rot)
        rot_cos = math.cos(cand_rot)
        
        dist_to_center = math.sqrt(cand_x**2 + cand_z**2)
        dist_left = cand_x - (-half_w) - item_w / 2.0
        dist_right = half_w - cand_x - item_w / 2.0
        dist_back = cand_z - (-half_l) - item_d / 2.0
        dist_front = half_l - cand_z - item_d / 2.0
        dist_to_min_wall = max(0.0, min(dist_left, dist_right, dist_back, dist_front))
        dist_to_back_wall = max(0.0, dist_back)
        
        # Wall alignment (closer to 1.0 if rotation is parallel/orthogonal to walls)
        angle_mod = abs(cand_rot % (math.pi / 2.0))
        wall_alignment = 1.0 - (min(angle_mod, math.pi / 2.0 - angle_mod) / (math.pi / 4.0))
        
        # Clearance to already placed furniture items
        current_box = BoundingBox2D(cand_x, cand_z, item_w, item_d, cand_rot)
        clearance_to_nearest = 5.0
        if placed_boxes:
            clearance_to_nearest = min(current_box.min_distance_to(b) for b in placed_boxes)
            
        vector = [
            rt_bed, rt_living, rt_dining, rt_office, rt_other,
            room_w, room_l, room_area, aspect_ratio,
            cat_sofa, cat_bed, cat_table, cat_chair, cat_storage, cat_decor,
            item_w, item_h, item_d, furn_footprint, min(item_price, 3000.0) / 1000.0,
            norm_x, norm_z, rot_sin, rot_cos,
            dist_to_center, dist_to_min_wall, dist_to_back_wall,
            wall_alignment, clearance_to_nearest
        ]
        return np.array(vector, dtype=np.float32)

class LayoutMLModel:
    """
    ML-Driven Furniture Layout Recommendation Model.
    Generates placement candidates, extracts spatial/geometric features,
    scores placements using a trained scikit-learn regressor, applies hard physical constraints,
    and returns the optimal feasible arrangement with human-readable rationale.
    """

    _instance = None

    def __init__(self, model_version: str = "v001"):
        self.model_version = model_version
        self.model: Optional[RandomForestRegressor] = None
        self.metadata: Dict[str, Any] = {}
        self.is_loaded = False
        self.artifact_path = Path(settings.MODEL_ARTIFACT_DIR) / f"layout_model_{model_version}.joblib"
        self.metadata_path = Path(settings.MODEL_ARTIFACT_DIR) / f"layout_model_{model_version}.json"
        self.load()

    @classmethod
    def get_instance(cls) -> "LayoutMLModel":
        if cls._instance is None:
            cls._instance = LayoutMLModel()
        return cls._instance

    def load(self) -> bool:
        if self.artifact_path.exists():
            try:
                self.model = joblib.load(self.artifact_path)
                if self.metadata_path.exists():
                    with open(self.metadata_path, "r", encoding="utf-8") as f:
                        self.metadata = json.load(f)
                self.is_loaded = True
                logger.info(f"Loaded ML Layout Model '{self.model_version}' from {self.artifact_path}")
                return True
            except Exception as ex:
                logger.error(f"Failed to load layout model from {self.artifact_path}: {ex}")
                self.is_loaded = False
                return False
        else:
            logger.info(f"Layout model checkpoint not found at {self.artifact_path}. Operating in fallback mode.")
            self.is_loaded = False
            return False

    def generate_candidates(
        self,
        room_w: float,
        room_l: float,
        item_w: float,
        item_d: float,
        item_cat: str
    ) -> List[Tuple[float, float, float]]:
        """Generates diverse discrete candidate positions and orientations."""
        half_w = room_w / 2.0
        half_l = room_l / 2.0
        candidates: List[Tuple[float, float, float]] = []
        
        rotations = [0.0, math.pi / 2.0, math.pi, -math.pi / 2.0]
        
        # 1. Back wall anchored placements
        for rot in [0.0, math.pi]:
            z_pos = -half_l + (item_d / 2.0) + 0.1
            for x_ratio in [-0.6, -0.3, 0.0, 0.3, 0.6]:
                candidates.append((x_ratio * (half_w - item_w / 2.0), z_pos, rot))
                
        # 2. Side wall anchored placements
        for rot in [math.pi / 2.0, -math.pi / 2.0]:
            x_pos_left = -half_w + (item_w / 2.0) + 0.1
            x_pos_right = half_w - (item_w / 2.0) - 0.1
            for z_ratio in [-0.5, 0.0, 0.5]:
                z_val = z_ratio * (half_l - item_d / 2.0)
                candidates.append((x_pos_left, z_val, rot))
                candidates.append((x_pos_right, z_val, rot))
                
        # 3. Center and conversational zone placements
        candidates.append((0.0, 0.0, 0.0))
        candidates.append((0.0, 0.5, 0.0))
        candidates.append((0.0, -0.5, 0.0))
        
        # 4. Corner accent placements
        for cx in [-half_w + item_w / 2.0 + 0.3, half_w - item_w / 2.0 - 0.3]:
            for cz in [-half_l + item_d / 2.0 + 0.3, half_l - item_d / 2.0 - 0.3]:
                candidates.append((cx, cz, 0.0))
                
        return candidates

    def score_placement(
        self,
        features: np.ndarray
    ) -> float:
        """Scores candidate placement using the trained model, or heuristic fallback."""
        if self.is_loaded and self.model is not None:
            try:
                pred = float(self.model.predict(features.reshape(1, -1))[0])
                return max(0.0, min(1.0, pred))
            except Exception:
                pass
                
        # Explainable fallback heuristic score
        norm_x, norm_z = features[20], features[21]
        dist_wall = features[25]
        wall_align = features[27]
        clearance = features[28]
        
        # Reward wall proximity for non-central items, reward alignment and generous clearance
        score = 0.5 + 0.2 * wall_align + 0.2 * min(1.0, clearance / 0.8) - 0.1 * min(1.0, dist_wall / 2.0)
        return float(max(0.1, min(0.99, score)))

    def rank_placements(
        self,
        room_w: float,
        room_l: float,
        room_type: str,
        furniture_item: Any,
        placed_boxes: List[BoundingBox2D]
    ) -> Optional[Dict[str, Any]]:
        """
        Ranks all feasible candidate placements and selects the top-scoring non-colliding candidate.
        """
        candidates = self.generate_candidates(
            room_w, room_l,
            furniture_item.width_m, furniture_item.depth_m,
            furniture_item.category
        )
        
        scored_candidates: List[Dict[str, Any]] = []
        
        for cand_x, cand_z, cand_rot in candidates:
            box = BoundingBox2D(cand_x, cand_z, furniture_item.width_m, furniture_item.depth_m, cand_rot)
            
            # 1. Hard Physical Constraint: Must be fully inside room
            if not box.is_inside_room(room_w, room_l):
                continue
                
            # 2. Hard Physical Constraint: Must not intersect already placed furniture
            collision = any(box.intersects(pb, margin=0.08) for pb in placed_boxes)
            if collision:
                continue
                
            # 3. Extract structured features
            features = LayoutFeatureExtractor.extract_features(
                room_w=room_w,
                room_l=room_l,
                room_type=room_type,
                item_category=furniture_item.category,
                item_w=furniture_item.width_m,
                item_h=furniture_item.height_m,
                item_d=furniture_item.depth_m,
                item_price=furniture_item.price_estimate,
                cand_x=cand_x,
                cand_z=cand_z,
                cand_rot=cand_rot,
                placed_boxes=placed_boxes
            )
            
            # 4. Predict ML suitability score
            score = self.score_placement(features)
            
            scored_candidates.append({
                "x": cand_x,
                "z": cand_z,
                "rot": cand_rot,
                "box": box,
                "score": score,
                "features": features
            })
            
        if not scored_candidates:
            return None
            
        # Select best candidate
        scored_candidates.sort(key=lambda c: c["score"], reverse=True)
        best = scored_candidates[0]
        
        # Build human-readable explanation
        wall_dist = best["features"][25]
        clearance = best["features"][28]
        model_source = "ML trained ranking model" if self.is_loaded else "geometric heuristic fallback"
        
        reason = (
            f"Selected by {model_source} with suitability score {best['score']:.2f}. "
            f"Preserves {clearance:.2f}m walking corridor and maintains {wall_dist:.2f}m wall alignment."
        )
        
        return {
            "pos_x": round(best["x"], 2),
            "pos_y": 0.0,
            "pos_z": round(best["z"], 2),
            "rot_y": round(best["rot"], 2),
            "score": round(best["score"], 4),
            "box": best["box"],
            "reason": reason
        }
