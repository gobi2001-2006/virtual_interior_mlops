import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, JSON, DateTime, ForeignKey
from backend.app.db.base import Base, utc_now

class TrainingJob(Base):
    __tablename__ = "training_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String(64), unique=True, index=True, nullable=False)
    job_type = Column(String(50), default="room_classification", nullable=False)  # room_classification, layout_recommendation
    status = Column(String(30), default="QUEUED", nullable=False)  # QUEUED, RUNNING, COMPLETED, FAILED
    model_version_target = Column(String(50), nullable=False)
    epochs = Column(Integer, default=5, nullable=False)
    batch_size = Column(Integer, default=16, nullable=False)
    learning_rate = Column(Float, default=0.001, nullable=False)
    dataset_size = Column(Integer, default=0, nullable=False)
    training_history = Column(JSON, nullable=True)
    error_message = Column(String(1000), nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)

class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    version_tag = Column(String(50), unique=True, index=True, nullable=False)
    model_type = Column(String(50), default="room_classifier", nullable=False) # room_classifier, furniture_layout_recommender
    architecture = Column(String(100), default="MobileNetV3-Small", nullable=False)
    weights_path = Column(String(500), nullable=False)
    metadata_path = Column(String(500), nullable=True)
    accuracy = Column(Float, nullable=True)
    macro_f1 = Column(Float, nullable=True)
    is_active = Column(Boolean, default=False, nullable=False)
    is_promoted = Column(Boolean, default=False, nullable=False)
    promoted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)

class ModelEvaluation(Base):
    __tablename__ = "model_evaluations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    model_version_tag = Column(String(50), index=True, nullable=False)
    dataset_name = Column(String(100), default="test_split", nullable=False)
    sample_count = Column(Integer, default=0, nullable=False)
    accuracy = Column(Float, nullable=False)
    macro_f1 = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    per_class_metrics = Column(JSON, nullable=False)
    confusion_matrix = Column(JSON, nullable=False)
    passed_threshold = Column(Boolean, default=False, nullable=False)
    evaluated_at = Column(DateTime, default=utc_now, nullable=False)

class ExperimentRun(Base):
    __tablename__ = "experiment_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    run_name = Column(String(100), nullable=False)
    mlflow_run_id = Column(String(100), nullable=True)
    parameters = Column(JSON, nullable=False)
    metrics = Column(JSON, nullable=False)
    status = Column(String(50), default="FINISHED", nullable=False)
    artifact_uri = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)

class PredictionEvent(Base):
    __tablename__ = "prediction_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    model_version = Column(String(50), index=True, nullable=False)
    predicted_room_type = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    latency_ms = Column(Float, nullable=False)
    is_demo_fallback = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
