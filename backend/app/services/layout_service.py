import math
from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy.orm import Session

from backend.app.models.furniture import FurnitureItem
from backend.app.models.layout import Layout, LayoutItem
from backend.app.schemas.layout import LayoutRecommendRequest, LayoutWarning
from backend.app.core.logging import logger
from backend.app.ml.layout_model import BoundingBox2D, LayoutMLModel

class LayoutEngine:
    """
    ML-Driven Furniture Layout Recommendation Engine.
    Uses trained LayoutMLModel to evaluate candidate placements, rank them,
    and enforce room boundary and non-intersection constraints.
    Falls back gracefully to deterministic spatial rules if no ML model is loaded.
    """

    @classmethod
    def generate_recommendations(
        cls,
        db: Session,
        request: LayoutRecommendRequest
    ) -> Tuple[List[Dict[str, Any]], List[LayoutWarning], str]:
        room_type = (request.room_type or "LivingRoom").strip()
        room_w = max(2.5, request.width_m or 4.0)
        room_l = max(2.5, request.length_m or 5.0)
        
        warnings: List[LayoutWarning] = []
        if room_w < 3.0 or room_l < 3.0:
            warnings.append(LayoutWarning(
                code="TIGHT_DIMENSIONS",
                message=f"Room dimensions ({room_w:.1f}m x {room_l:.1f}m) are compact. Recommendations prioritize space-saving furniture."
            ))
            
        # Fetch suitable furniture items from database
        items = db.query(FurnitureItem).all()
        by_category: Dict[str, List[FurnitureItem]] = {}
        for item in items:
            cat = item.category.lower()
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(item)
            
        placed_boxes: List[BoundingBox2D] = []
        placements: List[Dict[str, Any]] = []
        
        def choose_item(cat_name: str) -> Optional[FurnitureItem]:
            candidates = by_category.get(cat_name.lower(), [])
            if not candidates:
                # Fuzzy fallback
                for c_key, c_items in by_category.items():
                    if cat_name.lower() in c_key or c_key in cat_name.lower():
                        candidates = c_items
                        break
            if not candidates:
                return None
            # Filter by style if available
            styled = [c for c in candidates if c.style.lower() == (request.style or "").lower()]
            return styled[0] if styled else candidates[0]

        # Determine target furniture composition for the room type
        target_categories = cls._get_room_composition(room_type)
        
        layout_model = LayoutMLModel.get_instance()
        is_ml_active = layout_model.is_loaded
        model_version = f"layout_{layout_model.model_version}" if is_ml_active else "fallback_deterministic"
        
        logger.info(f"Generating layout recommendations for '{room_type}' using model: {model_version}")
        
        for cat_name in target_categories:
            item = choose_item(cat_name)
            if not item:
                continue
                
            # Use ML Candidate Ranking if model is active
            if is_ml_active:
                placement_res = layout_model.rank_placements(
                    room_w=room_w,
                    room_l=room_l,
                    room_type=room_type,
                    furniture_item=item,
                    placed_boxes=placed_boxes
                )
                if placement_res:
                    placed_boxes.append(placement_res["box"])
                    placements.append({
                        "furniture": item,
                        "pos_x": placement_res["pos_x"],
                        "pos_y": placement_res["pos_y"],
                        "pos_z": placement_res["pos_z"],
                        "rot_y": placement_res["rot_y"],
                        "ml_score": placement_res["score"],
                        "reason": placement_res["reason"]
                    })
                else:
                    warnings.append(LayoutWarning(
                        code="ITEM_SKIPPED_CLEARANCE",
                        message=f"Could not place {item.name} without violating minimum circulation clearances."
                    ))
            else:
                # Fallback to deterministic placement heuristics
                cls._place_heuristic(item, room_w, room_l, room_type, placements, placed_boxes, warnings)

        # Clearance safety audit
        for i in range(len(placed_boxes)):
            for j in range(i + 1, len(placed_boxes)):
                dist = placed_boxes[i].min_distance_to(placed_boxes[j])
                if dist < 0.40:
                    warnings.append(LayoutWarning(
                        code="TIGHT_CLEARANCE",
                        message=f"Clearance between {placements[i]['furniture'].name} and {placements[j]['furniture'].name} is {dist:.2f}m."
                    ))

        return placements, warnings, model_version

    @classmethod
    def _get_room_composition(cls, room_type: str) -> List[str]:
        rt = room_type.lower()
        if "bed" in rt:
            return ["Bed", "Side table", "Side table", "Wardrobe", "Plant"]
        elif "living" in rt:
            return ["Rug", "Sofa", "Coffee table", "Armchair", "TV unit", "Plant"]
        elif "dining" in rt:
            return ["Dining table", "Chair", "Chair", "Chair", "Chair", "Plant"]
        elif "office" in rt:
            return ["Desk", "Chair", "Bookshelf", "Plant", "Armchair"]
        elif "bath" in rt:
            return ["Plant", "Side table"]
        elif "kitchen" in rt:
            return ["Dining table", "Chair", "Chair", "Plant"]
        else:
            return ["Desk", "Chair", "Bookshelf", "Plant"]

    @classmethod
    def _place_heuristic(
        cls,
        item: FurnitureItem,
        rw: float,
        rl: float,
        room_type: str,
        placements: List[Dict[str, Any]],
        placed_boxes: List[BoundingBox2D],
        warnings: List[LayoutWarning]
    ):
        half_w, half_l = rw / 2.0, rl / 2.0
        cat = item.category.lower()
        
        if "bed" in cat:
            pos_x, pos_z, rot_y = 0.0, -half_l + (item.depth_m / 2.0) + 0.1, 0.0
            reason = "Deterministic anchor: Bed centered against main wall for restful access."
        elif "sofa" in cat:
            pos_x, pos_z, rot_y = 0.0, -half_l + (item.depth_m / 2.0) + 0.2, 0.0
            reason = "Deterministic anchor: Sofa aligned along perimeter wall facing focal center."
        elif "dining table" in cat or "rug" in cat:
            pos_x, pos_z, rot_y = 0.0, 0.0, 0.0
            reason = "Deterministic placement: Centered in room to maintain equal circulation perimeter."
        elif "coffee table" in cat and placed_boxes:
            pos_x, pos_z, rot_y = 0.0, placed_boxes[0].z + (item.depth_m / 2.0) + 0.5, 0.0
            reason = "Deterministic placement: Positioned 0.5m in front of primary seating."
        elif "wardrobe" in cat or "bookshelf" in cat:
            pos_x, pos_z, rot_y = half_w - (item.depth_m / 2.0) - 0.05, 0.3, -math.pi / 2.0
            reason = "Deterministic placement: Storage arranged flush along side wall."
        elif "side table" in cat and placed_boxes:
            side = -1.0 if len([p for p in placements if "side table" in p["furniture"].category.lower()]) == 0 else 1.0
            pos_x = side * (placed_boxes[0].width / 2.0 + item.width_m / 2.0 + 0.08)
            pos_z = placed_boxes[0].z
            rot_y = 0.0
            reason = f"Deterministic placement: Nightstand placed on {'left' if side < 0 else 'right'} flank."
        else:
            # Corner accent
            pos_x, pos_z, rot_y = -half_w + 0.45, half_l - 0.45, 0.0
            reason = "Deterministic placement: Accent item positioned in open corner boundary."

        box = BoundingBox2D(pos_x, pos_z, item.width_m, item.depth_m, rot_y)
        if box.is_inside_room(rw, rl) and not any(box.intersects(pb) for pb in placed_boxes):
            placed_boxes.append(box)
            placements.append({
                "furniture": item,
                "pos_x": round(pos_x, 2),
                "pos_y": 0.0,
                "pos_z": round(pos_z, 2),
                "rot_y": round(rot_y, 2),
                "ml_score": 0.75,
                "reason": reason
            })
