import io
import json
from pathlib import Path
import pytest
import numpy as np
from PIL import Image
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.core.config import settings
from backend.app.ml.inference import InferenceService
from backend.app.ml.model import RoomClassifier

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(autouse=True)
def ensure_v003_loaded():
    """Ensure v003 model is loaded before each test in this module."""
    InferenceService.get_instance().load_model("v003")

def test_model_v003_loading_and_architecture():
    """
    Verifies that model_v003.pth loads cleanly into a 6-class MobileNetV3-Small architecture on CPU.
    """
    inf = InferenceService.get_instance()
    loaded = inf.load_model("v003")
    assert loaded is True, "Failed to load model_v003.pth checkpoint"
    assert inf.is_trained is True
    assert inf.loaded_version == "v003"
    assert inf.device == "cpu"
    assert isinstance(inf.current_model, RoomClassifier)
    assert len(inf.classes) == 6
    assert "Other" not in inf.classes

def test_checkpoint_and_class_order_validation():
    """
    Verifies class ordering against model_v003.json metadata and class_mapping.json.
    """
    inf = InferenceService.get_instance()
    metadata_path = Path(settings.MODEL_ARTIFACT_DIR) / "model_v003.json"
    assert metadata_path.exists(), "Metadata file model_v003.json must exist"

    with open(metadata_path, "r") as f:
        meta = json.load(f)

    # In metadata, 6 interior classes should match our active classes
    meta_classes = [c for c in meta["classes"] if c != "Other"]
    assert len(meta_classes) == 6
    for cls in inf.classes:
        assert cls in meta_classes

    # Check class_mapping.json if present
    mapping_path = Path(settings.MODEL_ARTIFACT_DIR) / "class_mapping.json"
    if mapping_path.exists():
        with open(mapping_path, "r") as f:
            mapping = json.load(f)
        for cls in inf.classes:
            assert cls in mapping

def test_cpu_inference_on_synthetic_image():
    """
    Verifies CPU inference, finite probabilities summing to ~1.0, and 6-class dictionary.
    """
    inf = InferenceService.get_instance()
    # Create synthetic test RGB image
    img = Image.new("RGB", (256, 256), color=(140, 180, 210))
    result = inf.predict(img)

    assert result["model_version"] == "v003"
    assert result["predicted_room"] in inf.classes
    assert 0.0 <= result["confidence"] <= 1.0
    assert result["is_demo_fallback"] is False
    assert result["latency_ms"] >= 0.0

    # Probabilities verification
    probs = result["probabilities"]
    assert len(probs) == 6
    for cls in inf.classes:
        assert cls in probs
        val = probs[cls]
        assert isinstance(val, float)
        assert np.isfinite(val)
        assert 0.0 <= val <= 1.0

    # Ensure probabilities sum approximately to 1.0
    prob_sum = sum(probs.values())
    assert abs(prob_sum - 1.0) < 0.05

def test_predict_endpoint_v1_and_default_routes(client):
    """
    Tests both POST /api/v1/rooms/predict and POST /api/rooms/predict with a valid JPEG image.
    """
    # Create in-memory JPEG image bytes
    img = Image.new("RGB", (128, 128), color=(200, 150, 100))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    # Test /api/v1/rooms/predict
    response_v1 = client.post(
        "/api/v1/rooms/predict",
        files={"file": ("test_room.jpg", buf.getvalue(), "image/jpeg")}
    )
    assert response_v1.status_code == 200
    data_v1 = response_v1.json()
    assert data_v1["model_version"] == "v003"
    assert "predicted_room" in data_v1
    assert "confidence" in data_v1
    assert "probabilities" in data_v1
    assert len(data_v1["probabilities"]) == 6

    # Test /api/rooms/predict
    buf.seek(0)
    response_default = client.post(
        "/api/rooms/predict",
        files={"file": ("test_room.jpg", buf.getvalue(), "image/jpeg")}
    )
    assert response_default.status_code == 200
    data_default = response_default.json()
    assert data_default["predicted_room"] == data_v1["predicted_room"]

def test_predict_endpoint_unsupported_image_format(client):
    """
    Verifies that unsupported file types (e.g. text/plain) return 400 Bad Request.
    """
    response = client.post(
        "/api/v1/rooms/predict",
        files={"file": ("document.txt", b"plain text content", "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported image type" in response.json()["detail"]

def test_predict_endpoint_corrupted_image(client):
    """
    Verifies that corrupted image bytes with image/jpeg header return 400 Bad Request.
    """
    corrupt_bytes = b"\xff\xd8\xff\xe0" + b"random_corrupt_data" * 20
    response = client.post(
        "/api/v1/rooms/predict",
        files={"file": ("corrupt.jpg", corrupt_bytes, "image/jpeg")}
    )
    assert response.status_code == 400
    assert "Corrupted or invalid image file" in response.json()["detail"]

def test_predict_endpoint_oversized_upload(client):
    """
    Verifies that files exceeding MAX_UPLOAD_SIZE_MB return 413 Payload Too Large.
    """
    oversized_bytes = b"0" * ((settings.MAX_UPLOAD_SIZE_MB + 1) * 1024 * 1024)
    response = client.post(
        "/api/v1/rooms/predict",
        files={"file": ("oversized.jpg", oversized_bytes, "image/jpeg")}
    )
    assert response.status_code == 413
    assert "exceeds maximum allowed size" in response.json()["detail"]

def test_missing_model_checkpoint_graceful_handling():
    """
    Verifies controlled handling when a requested checkpoint does not exist.
    """
    inf = InferenceService.get_instance()
    loaded = inf.load_model("v_non_existent_999")
    assert loaded is False
    assert inf.is_trained is False

    # Predict should safely engage demo fallback without crash
    img = Image.new("RGB", (64, 64), color="blue")
    result = inf.predict(img)
    assert result["is_demo_fallback"] is True
    assert "demo-fallback" in result["model_version"]
    assert len(result["probabilities"]) == 6

    # Restore v003
    inf.load_model("v003")

def test_room_model_status_endpoint(client):
    """
    Tests GET /api/rooms/model-status and GET /api/v1/rooms/model-status.
    """
    response = client.get("/api/v1/rooms/model-status")
    assert response.status_code == 200
    data = response.json()
    assert data["model_version"] == "v003"
    assert data["is_loaded"] is True
    assert data["is_trained"] is True
    assert data["device"] == "cpu"
    assert data["architecture"] == "MobileNetV3-Small"
    assert data["num_classes"] == 6
    assert len(data["classes"]) == 6
    # Verify no filesystem paths leaked
    assert "/" not in data["model_version"]
    assert "\\" not in data["model_version"]
