import os
import uuid
from datetime import datetime, timezone
from backend.app.models.mlops import TrainingJob, ModelVersion, ModelEvaluation
from backend.app.models.feedback import UserFeedback
from backend.app.models.room import Room
from backend.app.core.config import settings

def test_mlops_status(client):
    response = client.get("/api/mlops/status")
    assert response.status_code == 200
    data = response.json()
    assert "active_model_version" in data
    assert "model_architecture" in data
    assert data["model_architecture"] == "MobileNetV3-Small"
    assert "supported_classes" in data
    assert len(data["supported_classes"]) == 7

def test_mlops_metrics(client):
    response = client.get("/api/mlops/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_predictions" in data
    assert "average_latency_ms" in data

def test_retraining_insufficient_data_rejection(client):
    # Attempt to start retraining when insufficient approved data exists
    response = client.post(
        "/api/mlops/train",
        json={"epochs": 2, "batch_size": 8, "learning_rate": 0.001, "include_approved_feedback": True}
    )
    assert response.status_code == 400
    assert "Insufficient approved training data" in response.json()["detail"]

def test_retraining_sufficient_approved_samples(client, db_session, dummy_room_image):
    # Create a room
    room = Room(
        name="Retrain Source Room",
        image_path="/uploads/dummy_sample.jpg",
        style_preference="modern",
        budget_preference="medium",
        width_m=4.0,
        length_m=5.0,
        height_m=2.8
    )
    db_session.add(room)
    db_session.commit()

    # Create 10 approved feedback records with verified corrected room types
    for i in range(settings.MIN_APPROVED_FEEDBACK_SAMPLES):
        fb = UserFeedback(
            room_id=room.id,
            model_version="v001",
            is_liked=True,
            star_rating=5,
            corrected_room_type="Bedroom",
            is_approved_for_training=True,
            approval_notes=f"Admin verified sample #{i+1}"
        )
        db_session.add(fb)
    db_session.commit()

    # Trigger retraining - should now pass validation and return HTTP 202
    response = client.post(
        "/api/mlops/train",
        json={"epochs": 1, "batch_size": 4, "learning_rate": 0.001, "include_approved_feedback": True}
    )
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "QUEUED"
    assert "job_id" in data

def test_duplicate_training_job_prevention(client, db_session):
    # Insert a currently RUNNING training job
    existing_job = TrainingJob(
        job_id=f"job_running_{uuid.uuid4().hex[:8]}",
        status="RUNNING",
        model_version_target="v_test_concurrent",
        epochs=5,
        batch_size=16,
        learning_rate=0.001,
        dataset_size=100
    )
    db_session.add(existing_job)
    db_session.commit()

    # Attempt to launch another concurrent training job
    response = client.post(
        "/api/mlops/train",
        json={"epochs": 2, "batch_size": 8, "learning_rate": 0.001}
    )
    assert response.status_code == 409
    assert "currently in progress" in response.json()["detail"]

def test_training_job_failure_status(client, db_session):
    # Insert a FAILED job
    job_id = f"job_fail_{uuid.uuid4().hex[:8]}"
    failed_job = TrainingJob(
        job_id=job_id,
        status="FAILED",
        model_version_target="v_fail_test",
        epochs=3,
        batch_size=8,
        learning_rate=0.001,
        dataset_size=20,
        error_message="Corrupted image headers in batch 2"
    )
    db_session.add(failed_job)
    db_session.commit()

    # Query status
    response = client.get(f"/api/mlops/train/{job_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "FAILED"
    assert data["error_message"] == "Corrupted image headers in batch 2"

def test_candidate_evaluation_failure_rejection(client, db_session):
    version_tag = f"v_candidate_fail_{uuid.uuid4().hex[:6]}"
    dummy_weights = os.path.join(settings.MODEL_ARTIFACT_DIR, f"model_{version_tag}.pth")
    with open(dummy_weights, "wb") as f:
        f.write(b"dummy model weights bytes")

    # Candidate with low accuracy that failed evaluation threshold
    candidate = ModelVersion(
        version_tag=version_tag,
        architecture="MobileNetV3-Small",
        weights_path=dummy_weights,
        accuracy=0.22,
        macro_f1=0.15,
        is_active=False,
        is_promoted=False
    )
    db_session.add(candidate)
    
    evaluation = ModelEvaluation(
        model_version_tag=version_tag,
        dataset_name="held_out_test_split",
        sample_count=20,
        accuracy=0.22,
        macro_f1=0.15,
        precision=0.20,
        recall=0.22,
        per_class_metrics={},
        confusion_matrix=[],
        passed_threshold=False
    )
    db_session.add(evaluation)
    db_session.commit()

    # Promotion should be rejected with 400
    response = client.post(f"/api/mlops/promote/{version_tag}")
    assert response.status_code == 400
    assert "Candidate has not passed quality evaluation criteria" in response.json()["detail"]

def test_model_promotion_guard_unregistered(client):
    # Attempt to promote non-existent version
    response = client.post("/api/mlops/promote/v_non_existent_999")
    assert response.status_code == 404

def test_successful_promotion_after_passing_quality_gates(client, db_session):
    version_tag = f"v_candidate_pass_{uuid.uuid4().hex[:6]}"
    dummy_weights = os.path.join(settings.MODEL_ARTIFACT_DIR, f"model_{version_tag}.pth")
    with open(dummy_weights, "wb") as f:
        f.write(b"dummy model weights bytes")

    # Candidate that passed threshold
    candidate = ModelVersion(
        version_tag=version_tag,
        architecture="MobileNetV3-Small",
        weights_path=dummy_weights,
        accuracy=0.88,
        macro_f1=0.85,
        is_active=False,
        is_promoted=False
    )
    db_session.add(candidate)

    evaluation = ModelEvaluation(
        model_version_tag=version_tag,
        dataset_name="held_out_test_split",
        sample_count=50,
        accuracy=0.88,
        macro_f1=0.85,
        precision=0.87,
        recall=0.86,
        per_class_metrics={},
        confusion_matrix=[],
        passed_threshold=True
    )
    db_session.add(evaluation)
    db_session.commit()

    # Promotion should succeed
    response = client.post(f"/api/mlops/promote/{version_tag}")
    assert response.status_code == 200
    data = response.json()
    assert data["version_tag"] == version_tag
    assert data["is_active"] is True
    assert data["is_promoted"] is True
    assert data["promoted_at"] is not None
