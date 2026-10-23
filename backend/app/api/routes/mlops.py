from typing import List, Dict, Any, Optional
import json
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.db.session import get_db
from backend.app.core.config import settings
from backend.app.core.security import verify_admin_api_key
from backend.app.models.room import Room
from backend.app.models.layout import Layout
from backend.app.models.feedback import UserFeedback
from backend.app.models.mlops import (
    TrainingJob,
    ModelVersion,
    ModelEvaluation,
    ExperimentRun,
    PredictionEvent
)
from backend.app.schemas.mlops import (
    MLOpsStatusResponse,
    MLOpsMetricsResponse,
    TrainingJobRequest,
    TrainingJobResponse,
    ModelVersionResponse,
    ModelEvaluationResponse
)
from backend.app.services.retraining_service import RetrainingService
from backend.app.services.model_registry_service import ModelRegistryService
from backend.app.ml.inference import InferenceService
from backend.app.ml.layout_model import LayoutMLModel

router = APIRouter(prefix="/mlops", tags=["MLOps"])

@router.get("/status", response_model=MLOpsStatusResponse)
def get_mlops_status(db: Session = Depends(get_db)):
    inf_service = InferenceService.get_instance()
    layout_service = LayoutMLModel.get_instance()
    
    total_analyses = db.query(Room).count()
    total_designs = db.query(Layout).count()
    total_feedback = db.query(UserFeedback).count()
    approved_feedback = db.query(UserFeedback).filter(
        UserFeedback.is_approved_for_training == True
    ).count()
    
    active_jobs = db.query(TrainingJob).filter(TrainingJob.status == "RUNNING").count()
    recent_jobs = db.query(TrainingJob).order_by(TrainingJob.created_at.desc()).limit(5).all()
    models = db.query(ModelVersion).order_by(ModelVersion.created_at.desc()).all()
    
    latest_eval = db.query(ModelEvaluation).order_by(ModelEvaluation.evaluated_at.desc()).first()

    # Read dataset report if available
    dataset_report_path = Path("ml/data/processed/house_rooms/dataset_report.json")
    kaggle_status = "absent"
    kaggle_path = None
    if dataset_report_path.exists():
        try:
            with open(dataset_report_path, "r", encoding="utf-8") as f:
                d_report = json.load(f)
                kaggle_status = d_report.get("status", "absent")
                kaggle_path = d_report.get("expected_path")
        except Exception:
            pass

    return MLOpsStatusResponse(
        # Vision Classifier
        active_model_version=inf_service.loaded_version or settings.ACTIVE_MODEL_VERSION,
        is_trained_model_loaded=inf_service.is_trained,
        is_demo_fallback_active=not inf_service.is_trained,
        model_architecture="MobileNetV3-Small",
        supported_classes=settings.ROOM_CLASSES,
        # Layout Recommender
        active_layout_model_version=f"layout_{layout_service.model_version}" if layout_service.is_loaded else "fallback_deterministic",
        is_layout_model_loaded=layout_service.is_loaded,
        layout_model_architecture="RandomForestRegressor",
        layout_model_metrics=layout_service.metadata.get("metrics"),
        # Kaggle Ingestion Status
        kaggle_dataset_status=kaggle_status,
        kaggle_dataset_path=kaggle_path,
        # Telemetry
        total_room_analyses=total_analyses,
        total_saved_designs=total_designs,
        total_feedback_records=total_feedback,
        approved_feedback_samples=approved_feedback,
        min_approved_samples_required=settings.MIN_APPROVED_FEEDBACK_SAMPLES,
        retraining_permitted=(approved_feedback >= settings.MIN_APPROVED_FEEDBACK_SAMPLES),
        active_training_jobs_count=active_jobs,
        recent_training_jobs=[TrainingJobResponse.model_validate(j) for j in recent_jobs],
        available_models=[ModelVersionResponse.model_validate(m) for m in models],
        last_evaluation=ModelEvaluationResponse.model_validate(latest_eval) if latest_eval else None
    )

@router.get("/models", response_model=List[ModelVersionResponse])
def get_all_models(db: Session = Depends(get_db)):
    return ModelRegistryService.get_all_models(db)

@router.get("/metrics", response_model=MLOpsMetricsResponse)
def get_mlops_metrics(db: Session = Depends(get_db)):
    total_predictions = db.query(PredictionEvent).count()
    avg_latency = db.query(func.avg(PredictionEvent.latency_ms)).scalar() or 0.0

    class_counts = db.query(
        PredictionEvent.predicted_room_type,
        func.count(PredictionEvent.id)
    ).group_by(PredictionEvent.predicted_room_type).all()

    positives = db.query(UserFeedback).filter(
        (UserFeedback.is_liked == True) | (UserFeedback.star_rating >= 4)
    ).count()
    total_feedback = db.query(UserFeedback).count()
    sentiment_rate = round((positives / max(1, total_feedback)) * 100.0, 1)

    return MLOpsMetricsResponse(
        total_predictions=total_predictions,
        average_latency_ms=round(float(avg_latency), 2),
        prediction_volume_by_day={"today": total_predictions},
        predictions_by_class={cls: count for cls, count in class_counts},
        feedback_sentiment_rate=sentiment_rate
    )

@router.post("/train", response_model=TrainingJobResponse, status_code=status.HTTP_202_ACCEPTED)
def trigger_retraining(
    payload: TrainingJobRequest,
    db: Session = Depends(get_db),
    _authorized: bool = Depends(verify_admin_api_key)
):
    return RetrainingService.start_retraining_job(db, payload)

@router.get("/train/{job_id}", response_model=TrainingJobResponse)
def get_training_job_status(job_id: str, db: Session = Depends(get_db)):
    job = RetrainingService.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training job not found")
    return job

@router.post("/promote/{model_version}", response_model=ModelVersionResponse)
def promote_model_version(
    model_version: str,
    db: Session = Depends(get_db),
    _authorized: bool = Depends(verify_admin_api_key)
):
    return ModelRegistryService.promote_model(db, model_version)
