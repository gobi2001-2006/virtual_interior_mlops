import os
import uuid
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.db.base import utc_now
from backend.app.models.mlops import TrainingJob, ModelEvaluation
from backend.app.models.feedback import UserFeedback
from backend.app.models.room import Room
from backend.app.schemas.mlops import TrainingJobRequest
from backend.app.services.model_registry_service import ModelRegistryService
from backend.app.ml.train import train_classifier
from backend.app.db.session import SessionLocal

_training_lock = threading.Lock()

class RetrainingService:
    @staticmethod
    def get_job_by_id(db: Session, job_id: str) -> Optional[TrainingJob]:
        return db.query(TrainingJob).filter(TrainingJob.job_id == job_id).first()

    @staticmethod
    def get_recent_jobs(db: Session, limit: int = 10):
        return db.query(TrainingJob).order_by(TrainingJob.created_at.desc()).limit(limit).all()

    @staticmethod
    def start_retraining_job(db: Session, payload: TrainingJobRequest) -> TrainingJob:
        # 1. Prevent concurrent running/queued training jobs
        running_job = db.query(TrainingJob).filter(TrainingJob.status.in_(["RUNNING", "QUEUED"])).first()
        if running_job:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A training job ({running_job.job_id}) is currently in progress (status: {running_job.status}). Please wait for completion."
            )

        # 2. Check approved feedback records
        approved_feedbacks = db.query(UserFeedback).filter(
            UserFeedback.is_approved_for_training == True,
            UserFeedback.corrected_room_type.isnot(None)
        ).all()
        approved_count = len(approved_feedbacks)

        raw_data_dir = Path(settings.BASE_DIR) / "ml" / "data" / "raw"
        image_files = []
        if raw_data_dir.exists():
            for ext in [".jpg", ".jpeg", ".png", ".webp"]:
                image_files.extend(list(raw_data_dir.rglob(f"*{ext}")))

        # 3. Minimum Data Verification:
        # If include_approved_feedback is True (the standard workflow), require >= MIN_APPROVED_FEEDBACK_SAMPLES
        if payload.include_approved_feedback:
            if approved_count < settings.MIN_APPROVED_FEEDBACK_SAMPLES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Insufficient approved training data. Found {approved_count} approved feedback sample(s), "
                        f"but a minimum of {settings.MIN_APPROVED_FEEDBACK_SAMPLES} is required for retraining. "
                        "Please verify and approve more user-corrected room labels in the MLOps hub before retraining."
                    )
                )
        else:
            # If purely raw dataset retraining is requested:
            if len(image_files) < settings.MIN_APPROVED_FEEDBACK_SAMPLES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Insufficient raw training data. Found {len(image_files)} image(s) in ml/data/raw/, "
                        f"but a minimum of {settings.MIN_APPROVED_FEEDBACK_SAMPLES} is required."
                    )
                )

        # 4. Prepare extra feedback training tuples
        extra_samples: List[Tuple[str, int]] = []
        if payload.include_approved_feedback:
            for fb in approved_feedbacks:
                room = db.query(Room).filter(Room.id == fb.room_id).first()
                if room and fb.corrected_room_type in settings.ROOM_CLASSES:
                    clean_rel = room.image_path.lstrip("/").replace("uploads/", "")
                    disk_path = Path(settings.UPLOAD_DIR) / clean_rel
                    if disk_path.exists():
                        class_idx = settings.ROOM_CLASSES.index(fb.corrected_room_type)
                        extra_samples.append((str(disk_path.resolve()), class_idx))

        total_data_points = len(image_files) + len(extra_samples)

        # 5. Create QUEUED training job record in database
        timestamp_tag = utc_now().strftime("%Y%m%d_%H%M%S")
        version_target = f"v_{timestamp_tag}"
        job_id = f"train_job_{uuid.uuid4().hex[:10]}"

        job = TrainingJob(
            job_id=job_id,
            status="QUEUED",
            model_version_target=version_target,
            epochs=payload.epochs,
            batch_size=payload.batch_size,
            learning_rate=payload.learning_rate,
            dataset_size=total_data_points
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        # 6. Launch training in background worker thread
        thread = threading.Thread(
            target=RetrainingService._run_training_worker,
            args=(job_id, str(raw_data_dir), version_target, extra_samples, payload.epochs, payload.batch_size, payload.learning_rate),
            daemon=True
        )
        thread.start()

        logger.info(f"Queued training job {job_id} for candidate target version {version_target}")
        return job

    @staticmethod
    def _run_training_worker(
        job_id: str,
        data_dir: str,
        version_target: str,
        extra_samples: List[Tuple[str, int]],
        epochs: int,
        batch_size: int,
        lr: float
    ):
        with _training_lock:
            db: Session = SessionLocal()
            job = db.query(TrainingJob).filter(TrainingJob.job_id == job_id).first()
            if not job:
                db.close()
                return

            job.status = "RUNNING"
            job.started_at = datetime.utcnow()
            db.commit()

            try:
                metadata = train_classifier(
                    data_dir=data_dir,
                    output_dir=settings.MODEL_ARTIFACT_DIR,
                    version_tag=version_target,
                    extra_samples=extra_samples,
                    epochs=epochs,
                    batch_size=batch_size,
                    lr=lr
                )
                
                # Check metrics & gate evaluation
                test_metrics = metadata.get("test_metrics", {})
                acc = test_metrics.get("accuracy", 0.0)
                macro_f1 = test_metrics.get("macro_f1", 0.0)
                
                # Candidate model is promoted only if it passes evaluation thresholds AND is not synthetic demo data
                is_demo = metadata.get("is_synthetic_demo", False)
                passed = (acc >= settings.EVALUATION_ACCURACY_THRESHOLD) and not is_demo

                # Register candidate model in model_versions table (is_active=False by default)
                weights_path = os.path.join(settings.MODEL_ARTIFACT_DIR, f"model_{version_target}.pth")
                metadata_path = os.path.join(settings.MODEL_ARTIFACT_DIR, f"model_{version_target}.json")
                
                ModelRegistryService.register_model_version(
                    db=db,
                    version_tag=version_target,
                    weights_path=weights_path,
                    metadata_path=metadata_path,
                    accuracy=acc,
                    macro_f1=macro_f1
                )

                # Record ModelEvaluation
                eval_record = ModelEvaluation(
                    model_version_tag=version_target,
                    dataset_name="held_out_test_split",
                    sample_count=test_metrics.get("sample_count", 0),
                    accuracy=acc,
                    macro_f1=macro_f1,
                    precision=test_metrics.get("precision", 0.0),
                    recall=test_metrics.get("recall", 0.0),
                    per_class_metrics=test_metrics.get("per_class_metrics", {}),
                    confusion_matrix=test_metrics.get("confusion_matrix", []),
                    passed_threshold=passed
                )
                db.add(eval_record)

                job.status = "COMPLETED"
                job.training_history = metadata.get("training_history", [])
                job.completed_at = datetime.utcnow()
                db.commit()
                logger.info(f"Training job {job_id} completed successfully.")
            except Exception as e:
                logger.error(f"Training job {job_id} failed: {e}")
                job.status = "FAILED"
                job.error_message = str(e)
                job.completed_at = datetime.utcnow()
                db.commit()
            finally:
                db.close()
