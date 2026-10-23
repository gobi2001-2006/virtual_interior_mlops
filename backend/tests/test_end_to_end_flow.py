import io
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def create_test_image_bytes():
    file = io.BytesIO()
    image = Image.new("RGB", (128, 128), color=(180, 200, 220))
    image.save(file, format="JPEG")
    file.seek(0)
    return file


def test_complete_virtual_interior_workflow():
    # 1. Upload room photo and run classification
    img_bytes = create_test_image_bytes()
    analyze_resp = client.post(
        "/api/rooms/analyze",
        files={"file": ("room.jpg", img_bytes, "image/jpeg")},
        data={"name": "End to End Modern Suite", "length_m": "5.0", "width_m": "4.0", "height_m": "2.8"}
    )
    assert analyze_resp.status_code == 201
    room_data = analyze_resp.json()
    assert "id" in room_data
    assert "latest_prediction" in room_data
    pred = room_data["latest_prediction"]
    assert "predicted_room_type" in pred
    assert "confidence" in pred
    assert "model_version" in pred
    room_id = room_data["id"]
    predicted_type = pred["predicted_room_type"]

    # 2. Retrieve compatible furniture catalog items
    catalog_resp = client.get(f"/api/furniture?room_type={predicted_type}")
    assert catalog_resp.status_code == 200
    furniture_list = catalog_resp.json()
    assert len(furniture_list) > 0
    # Verify each card has visual fields
    assert "category" in furniture_list[0]
    assert "color_hex" in furniture_list[0]
    assert "image_url" in furniture_list[0]

    # 3. Generate ML-scored layout recommendation
    rec_resp = client.post(
        "/api/layouts/recommend",
        json={
            "room_id": room_id,
            "room_type": predicted_type,
            "style": "modern",
            "budget": "medium",
            "width_m": 4.0,
            "length_m": 5.0
        }
    )
    assert rec_resp.status_code == 201
    rec_data = rec_resp.json()
    assert "id" in rec_data
    assert "items" in rec_data
    assert "layout_model_version" in rec_data
    assert len(rec_data["items"]) > 0

    first_item = rec_data["items"][0]
    assert "ml_score" in first_item
    assert "placement_reason" in first_item
    assert "furniture" in first_item
    assert "category" in first_item["furniture"]
    assert "color_hex" in first_item["furniture"]

    # 4. Save a custom / modified layout
    custom_resp = client.post(
        "/api/layouts",
        json={
            "room_id": room_id,
            "name": "User Refined Modern Layout",
            "room_type": predicted_type,
            "style": "modern",
            "budget": "medium",
            "items": [
                {
                    "furniture_id": first_item["furniture"]["id"],
                    "pos_x": 0.0,
                    "pos_y": 0.0,
                    "pos_z": 0.0,
                    "rot_y": 0.0,
                    "scale_x": 1.0,
                    "scale_y": 1.0,
                    "scale_z": 1.0,
                    "placement_reason": "User placed in room center",
                    "ml_score": 0.95
                }
            ]
        }
    )
    assert custom_resp.status_code == 201
    custom_layout = custom_resp.json()
    custom_layout_id = custom_layout["id"]

    # 5. Submit user feedback
    feedback_resp = client.post(
        "/api/feedback",
        json={
            "room_id": room_id,
            "star_rating": 5,
            "is_liked": True,
            "comments": "High aesthetic quality and optimal circulation clearance."
        }
    )
    assert feedback_resp.status_code == 201
    feedback_data = feedback_resp.json()
    assert feedback_data["star_rating"] == 5
    # Quality gate: initial user submission is unapproved by default for safety
    assert feedback_data["is_approved_for_training"] is False
    fb_id = feedback_data["id"]

    # Admin reviews and approves the feedback for retraining
    approve_resp = client.post(
        f"/api/feedback/{fb_id}/approve",
        json={"is_approved_for_training": True, "approval_notes": "Verified high-quality placement"},
        headers={"X-Admin-API-Key": "admin-dev-secret-key-2026"}
    )
    assert approve_resp.status_code == 200
    assert approve_resp.json()["is_approved_for_training"] is True

    # 6. Check MLOps status endpoint for dual model governance
    mlops_resp = client.get("/api/mlops/status")
    assert mlops_resp.status_code == 200
    mlops_data = mlops_resp.json()
    assert "active_model_version" in mlops_data
    assert "active_layout_model_version" in mlops_data
    assert "is_layout_model_loaded" in mlops_data
    assert "layout_model_metrics" in mlops_data
    assert "kaggle_dataset_status" in mlops_data
    assert mlops_data["active_layout_model_version"] == "layout_v001"
