import pytest
import numpy as np
import math
from backend.app.ml.layout_model import (
    BoundingBox2D,
    LayoutFeatureExtractor,
    LayoutMLModel,
    FEATURE_NAMES
)
from backend.app.ml.train_layout_model import (
    generate_synthetic_layout_dataset,
    train_and_evaluate_layout_model
)

def test_bounding_box_intersection_and_clearance():
    b1 = BoundingBox2D(0.0, 0.0, 2.0, 1.0, 0.0)
    # Overlapping box
    b2 = BoundingBox2D(0.5, 0.2, 1.0, 1.0, 0.0)
    assert b1.intersects(b2) is True

    # Distant non-overlapping box
    b3 = BoundingBox2D(3.0, 3.0, 1.0, 1.0, 0.0)
    assert b1.intersects(b3) is False
    assert b1.min_distance_to(b3) > 1.0

def test_bounding_box_room_containment():
    # 4m x 5m room -> bounds are [-2, 2] x [-2.5, 2.5]
    box_inside = BoundingBox2D(0.0, 0.0, 2.0, 1.0, 0.0)
    assert box_inside.is_inside_room(4.0, 5.0) is True

    box_outside = BoundingBox2D(1.8, 0.0, 1.0, 1.0, 0.0) # max_x = 2.3 > 2.0
    assert box_outside.is_inside_room(4.0, 5.0) is False

def test_feature_extractor_shape_and_values():
    features = LayoutFeatureExtractor.extract_features(
        room_w=4.0,
        room_l=5.0,
        room_type="Bedroom",
        item_category="Bed",
        item_w=1.8,
        item_h=1.0,
        item_d=2.1,
        item_price=950.0,
        cand_x=0.0,
        cand_z=-1.4,
        cand_rot=0.0,
        placed_boxes=[]
    )
    assert isinstance(features, np.ndarray)
    assert len(features) == len(FEATURE_NAMES)
    assert features.dtype == np.float32
    # Verify bedroom one-hot is 1.0
    assert features[0] == 1.0 # room_type_bed
    # Verify bed category one-hot is 1.0
    assert features[10] == 1.0 # furn_cat_bed

def test_layout_model_candidate_generation():
    model = LayoutMLModel.get_instance()
    candidates = model.generate_candidates(
        room_w=4.0, room_l=5.0, item_w=1.8, item_d=2.1, item_cat="Bed"
    )
    assert len(candidates) > 10
    for x, z, rot in candidates:
        assert isinstance(x, float)
        assert isinstance(z, float)
        assert isinstance(rot, float)

def test_layout_model_scoring_and_constraints():
    model = LayoutMLModel.get_instance()
    dummy_item = type("Item", (), {
        "width_m": 1.8, "depth_m": 2.1, "height_m": 1.0,
        "price_estimate": 950.0, "category": "Bed"
    })()
    
    # Empty room placement
    placed = []
    res = model.rank_placements(4.0, 5.0, "Bedroom", dummy_item, placed)
    assert res is not None
    assert "pos_x" in res
    assert "pos_z" in res
    assert "score" in res
    assert 0.0 <= res["score"] <= 1.0
    assert "reason" in res

def test_synthetic_layout_dataset_generation():
    X, y, meta = generate_synthetic_layout_dataset(num_samples=100, seed=123)
    assert len(X) == 100
    assert len(y) == 100
    assert meta["dataset_provenance"] == "synthetic_architectural_design_principles_v1"
    assert np.all(y >= 0.0) and np.all(y <= 1.0)

def test_layout_training_and_metrics():
    metrics = train_and_evaluate_layout_model(
        version="v_test_eval",
        num_samples=200,
        seed=42
    )
    assert metrics["model_version"] == "v_test_eval"
    assert "metrics" in metrics
    assert "r2_score" in metrics["metrics"]
    assert "collision_rate" in metrics["metrics"]
    assert metrics["metrics"]["collision_rate"] == 0.0
