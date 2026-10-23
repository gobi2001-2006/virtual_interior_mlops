from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class TrainingJobRequest(BaseModel):
    epochs: int = Field(default=5, ge=1, le=50)
    batch_size: int = Field(default=16, ge=1, le=128)
    learning_rate: float = Field(default=0.001, gt=0.0)
    include_approved_feedback: bool = True

class TrainingJobResponse(BaseModel):
    id: str
    job_id: str
    job_type: str = "room_classification"
    status: str
    model_version_target: str
    epochs: int
    batch_size: int
    learning_rate: float
    dataset_size: int
    training_history: Optional[List[Dict[str, Any]]] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ModelEvaluationResponse(BaseModel):
    id: str
    model_version_tag: str
    dataset_name: str
    sample_count: int
    accuracy: float
    macro_f1: float
    precision: float
    recall: float
    per_class_metrics: Dict[str, Any]
    confusion_matrix: List[List[int]]
    passed_threshold: bool
    evaluated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ModelVersionResponse(BaseModel):
    id: str
    version_tag: str
    model_type: str = "room_classifier"
    architecture: str
    weights_path: str
    metadata_path: Optional[str]
    accuracy: Optional[float]
    macro_f1: Optional[float]
    is_active: bool
    is_promoted: bool
    promoted_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MLOpsStatusResponse(BaseModel):
    # Vision Room Classifier
    active_model_version: str
    is_trained_model_loaded: bool
    is_demo_fallback_active: bool
    model_architecture: str
    supported_classes: List[str]
    # ML Layout Recommender
    active_layout_model_version: str = "layout_v001"
    is_layout_model_loaded: bool = True
    layout_model_architecture: str = "RandomForestRegressor"
    layout_model_metrics: Optional[Dict[str, Any]] = None
    # Dataset Ingestion Status
    kaggle_dataset_status: str = "absent"
    kaggle_dataset_path: Optional[str] = None
    # Metrics and Retraining
    total_room_analyses: int
    total_saved_designs: int
    total_feedback_records: int
    approved_feedback_samples: int
    min_approved_samples_required: int
    retraining_permitted: bool
    active_training_jobs_count: int
    recent_training_jobs: List[TrainingJobResponse]
    available_models: List[ModelVersionResponse]
    last_evaluation: Optional[ModelEvaluationResponse] = None

class MLOpsMetricsResponse(BaseModel):
    total_predictions: int
    average_latency_ms: float
    prediction_volume_by_day: Dict[str, int]
    predictions_by_class: Dict[str, int]
    feedback_sentiment_rate: float
