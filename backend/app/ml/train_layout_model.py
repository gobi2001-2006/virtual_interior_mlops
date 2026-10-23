import os
import sys
import json
import joblib
import math
import random
import argparse
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Any
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from backend.app.core.config import settings
from backend.app.core.logging import logger, setup_logging
from backend.app.ml.layout_model import (
    BoundingBox2D,
    LayoutFeatureExtractor,
    FEATURE_NAMES,
    LayoutMLModel
)

def generate_synthetic_layout_dataset(
    num_samples: int = 1200,
    seed: int = 42
) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    Generates a mathematically grounded synthetic training dataset of candidate furniture placements
    and suitability scores derived from architectural and ergonomic interior design standards.
    """
    random.seed(seed)
    np.random.seed(seed)
    
    room_types = ["Bedroom", "LivingRoom", "DiningRoom", "HomeOffice", "Other"]
    
    furniture_templates = [
        {"cat": "Bed", "w": 1.8, "h": 1.0, "d": 2.1, "price": 950.0, "ideal_rooms": ["Bedroom"]},
        {"cat": "Side table", "w": 0.5, "h": 0.55, "d": 0.45, "price": 120.0, "ideal_rooms": ["Bedroom", "LivingRoom"]},
        {"cat": "Wardrobe", "w": 1.6, "h": 2.1, "d": 0.65, "price": 850.0, "ideal_rooms": ["Bedroom"]},
        {"cat": "Sofa", "w": 2.2, "h": 0.85, "d": 0.95, "price": 780.0, "ideal_rooms": ["LivingRoom"]},
        {"cat": "Coffee table", "w": 1.0, "h": 0.45, "d": 0.6, "price": 220.0, "ideal_rooms": ["LivingRoom"]},
        {"cat": "Armchair", "w": 0.85, "h": 0.85, "d": 0.85, "price": 320.0, "ideal_rooms": ["LivingRoom", "HomeOffice"]},
        {"cat": "TV unit", "w": 1.8, "h": 0.5, "d": 0.45, "price": 420.0, "ideal_rooms": ["LivingRoom"]},
        {"cat": "Dining table", "w": 1.8, "h": 0.76, "d": 0.9, "price": 680.0, "ideal_rooms": ["DiningRoom"]},
        {"cat": "Chair", "w": 0.5, "h": 0.85, "d": 0.5, "price": 110.0, "ideal_rooms": ["DiningRoom", "HomeOffice"]},
        {"cat": "Desk", "w": 1.4, "h": 0.75, "d": 0.7, "price": 390.0, "ideal_rooms": ["HomeOffice", "Bedroom"]},
        {"cat": "Plant", "w": 0.45, "h": 1.2, "d": 0.45, "price": 85.0, "ideal_rooms": ["LivingRoom", "Bedroom", "HomeOffice"]},
        {"cat": "Rug", "w": 2.5, "h": 0.02, "d": 2.0, "price": 250.0, "ideal_rooms": ["LivingRoom", "Bedroom"]}
    ]
    
    X_rows = []
    y_scores = []
    
    for _ in range(num_samples):
        # Sample room dimensions (typical residential ranges: 3.0m - 7.0m)
        rw = round(random.uniform(3.2, 6.5), 2)
        rl = round(random.uniform(3.5, 7.5), 2)
        rt = random.choice(room_types)
        
        # Pick template
        item = random.choice(furniture_templates)
        iw, ih, id_ = item["w"], item["h"], item["d"]
        iprice = item["price"]
        icat = item["cat"]
        
        half_w = rw / 2.0
        half_l = rl / 2.0
        
        # Simulate some already placed furniture
        placed_boxes: List[BoundingBox2D] = []
        if random.random() > 0.4:
            # Place an anchor item (e.g. main bed or sofa)
            anchor_z = -half_l + 1.1
            placed_boxes.append(BoundingBox2D(0.0, anchor_z, 2.0, 1.0, 0.0))
            
        # Generate either good, mediocre, or poor placement candidate
        placement_type = random.choices(["optimal", "acceptable", "poor"], weights=[0.45, 0.35, 0.20])[0]
        
        if placement_type == "optimal":
            # Architectural best practice placement
            if icat == "Bed":
                cx, cz, crot = 0.0, -half_l + id_ / 2.0 + 0.1, 0.0
                suitability = random.uniform(0.90, 0.98)
            elif icat == "Sofa":
                cx, cz, crot = 0.0, -half_l + id_ / 2.0 + 0.2, 0.0
                suitability = random.uniform(0.88, 0.96)
            elif icat == "Dining table":
                cx, cz, crot = 0.0, 0.0, 0.0
                suitability = random.uniform(0.92, 0.99)
            elif icat == "Wardrobe":
                cx, cz, crot = half_w - iw / 2.0 - 0.05, 0.2, math.pi / 2.0
                suitability = random.uniform(0.86, 0.94)
            elif icat == "Coffee table" and placed_boxes:
                # In front of sofa/anchor
                cx, cz, crot = 0.0, placed_boxes[0].z + id_ + 0.5, 0.0
                suitability = random.uniform(0.89, 0.97)
            else:
                # Wall or corner accent
                cx = (half_w - iw / 2.0 - 0.2) * (1 if random.random() > 0.5 else -1)
                cz = half_l - id_ / 2.0 - 0.2
                crot = 0.0
                suitability = random.uniform(0.80, 0.90)
                
        elif placement_type == "acceptable":
            # Feasible but sub-optimal
            cx = round(random.uniform(-half_w + iw, half_w - iw), 2)
            cz = round(random.uniform(-half_l + id_, half_l - id_), 2)
            crot = random.choice([0.0, math.pi / 2.0, math.pi])
            suitability = random.uniform(0.55, 0.78)
            
        else: # poor placement
            # Awkward placement in middle of room, awkward rotation, or cramped
            if random.random() > 0.5:
                # Squeezed with little clearance
                cx = 0.0
                cz = 0.0 if icat != "Dining table" else half_l - id_ / 2.0 - 0.05
                crot = random.uniform(0.2, 1.2) # unaligned angle
                suitability = random.uniform(0.10, 0.35)
            else:
                # Far from wall or blocking corridor
                cx = random.uniform(-0.5, 0.5)
                cz = random.uniform(-0.5, 0.5)
                crot = math.pi / 4.0
                suitability = random.uniform(0.15, 0.40)
                
        # Room compatibility penalty if placed in non-ideal room
        if rt not in item["ideal_rooms"] and "Other" not in item["ideal_rooms"]:
            suitability = max(0.1, suitability * 0.7)
            
        feat = LayoutFeatureExtractor.extract_features(
            room_w=rw,
            room_l=rl,
            room_type=rt,
            item_category=icat,
            item_w=iw,
            item_h=ih,
            item_d=id_,
            item_price=iprice,
            cand_x=cx,
            cand_z=cz,
            cand_rot=crot,
            placed_boxes=placed_boxes
        )
        
        X_rows.append(feat)
        y_scores.append(round(suitability, 4))
        
    X = np.array(X_rows, dtype=np.float32)
    y = np.array(y_scores, dtype=np.float32)
    
    meta = {
        "dataset_provenance": "synthetic_architectural_design_principles_v1",
        "sample_count": num_samples,
        "feature_count": len(FEATURE_NAMES),
        "feature_names": FEATURE_NAMES,
        "generator_seed": seed,
        "description": "Ergonomic circulation clearances, wall alignments, conversational zones, and room typology matches."
    }
    return X, y, meta

def train_and_evaluate_layout_model(
    version: str = "v001",
    num_samples: int = 1500,
    seed: int = 42
) -> Dict[str, Any]:
    setup_logging()
    logger.info(f"Starting ML Layout Recommendation Model training (Version: {version})...")
    
    # 1. Generate Dataset
    X, y, meta = generate_synthetic_layout_dataset(num_samples=num_samples, seed=seed)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed
    )
    
    logger.info(f"Train split: {len(X_train)} samples, Test split: {len(X_test)} samples")
    
    # 2. Train Regressor
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=4,
        random_state=seed,
        n_jobs=1
    )
    model.fit(X_train, y_train)
    
    # 3. Held-out Evaluation
    y_pred = model.predict(X_test)
    mse = float(mean_squared_error(y_test, y_pred))
    mae = float(mean_absolute_error(y_test, y_pred))
    r2 = float(r2_score(y_test, y_pred))
    
    # 4. Feasibility & Physical Constraint Simulation
    # Simulate 50 realistic test room layouts to calculate collision and out-of-bounds rates
    collision_count = 0
    out_of_bounds_count = 0
    clearance_violation_count = 0
    total_simulated_items = 0
    
    test_rooms = [
        ("Bedroom", 4.0, 5.0),
        ("LivingRoom", 5.0, 6.0),
        ("DiningRoom", 4.2, 4.8),
        ("HomeOffice", 3.5, 4.0)
    ]
    
    dummy_item = type("Item", (), {
        "width_m": 1.8, "depth_m": 2.0, "height_m": 1.0,
        "price_estimate": 800.0, "category": "Bed"
    })()
    
    layout_model_wrapper = LayoutMLModel.__new__(LayoutMLModel)
    layout_model_wrapper.model = model
    layout_model_wrapper.is_loaded = True
    
    for rt, rw, rl in test_rooms * 10:
        placed_boxes: List[BoundingBox2D] = []
        for _ in range(4):
            res = layout_model_wrapper.rank_placements(rw, rl, rt, dummy_item, placed_boxes)
            if res:
                box: BoundingBox2D = res["box"]
                total_simulated_items += 1
                if not box.is_inside_room(rw, rl):
                    out_of_bounds_count += 1
                if any(box.intersects(pb) for pb in placed_boxes):
                    collision_count += 1
                placed_boxes.append(box)
                
    collision_rate = float(collision_count / max(1, total_simulated_items))
    out_of_bounds_rate = float(out_of_bounds_count / max(1, total_simulated_items))
    feasible_layout_rate = float(1.0 - (collision_rate + out_of_bounds_rate))
    
    logger.info(f"Evaluation Metrics: MSE={mse:.4f}, MAE={mae:.4f}, R²={r2:.4f}")
    logger.info(f"Feasibility: Collision Rate={collision_rate:.2f}, Out-of-bounds Rate={out_of_bounds_rate:.2f}, Feasible Rate={feasible_layout_rate:.2f}")
    
    # 5. Save Artifacts
    artifact_dir = Path(settings.MODEL_ARTIFACT_DIR)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = artifact_dir / f"layout_model_{version}.joblib"
    meta_path = artifact_dir / f"layout_model_{version}.json"
    
    joblib.dump(model, model_path)
    
    # Feature importances
    importances = dict(zip(FEATURE_NAMES, [round(float(v), 4) for v in model.feature_importances_]))
    top_features = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:8]
    
    metrics = {
        "model_version": version,
        "model_type": "furniture_layout_recommender",
        "algorithm": "RandomForestRegressor",
        "weights_path": str(model_path),
        "dataset_provenance": meta["dataset_provenance"],
        "dataset_samples": len(X),
        "test_samples": len(X_test),
        "metrics": {
            "mse": round(mse, 4),
            "mae": round(mae, 4),
            "r2_score": round(r2, 4),
            "collision_rate": round(collision_rate, 4),
            "out_of_bounds_rate": round(out_of_bounds_rate, 4),
            "feasible_layout_rate": round(feasible_layout_rate, 4)
        },
        "top_features": dict(top_features),
        "quality_gate_passed": r2 >= 0.50 and collision_rate == 0.0
    }
    
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        
    logger.info(f"Saved layout model artifacts to {model_path} and {meta_path}")
    return metrics

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train ML Furniture Layout Recommendation Model")
    parser.add_argument("--version", default="v001", help="Target model version identifier")
    parser.add_argument("--samples", type=int, default=1500, help="Number of synthetic training examples")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()
    
    res = train_and_evaluate_layout_model(
        version=args.version,
        num_samples=args.samples,
        seed=args.seed
    )
    print("\n--- ML Layout Model Training Summary ---")
    print(json.dumps(res, indent=2))
