import os
import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.db.base import utc_now
from backend.app.models.mlops import ModelVersion, ModelEvaluation
from backend.app.ml.inference import InferenceService

class ModelRegistryService:
    @staticmethod
    def get_all_models(db: Session) -> List[ModelVersion]:
        return db.query(ModelVersion).order_by(ModelVersion.created_at.desc()).all()

    @staticmethod
    def get_active_model(db: Session) -> Optional[ModelVersion]:
        return db.query(ModelVersion).filter(ModelVersion.is_active == True).first()

    @staticmethod
    def get_model_by_version(db: Session, version_tag: str) -> Optional[ModelVersion]:
        return db.query(ModelVersion).filter(ModelVersion.version_tag == version_tag).first()

    @staticmethod
    def register_model_version(
        db: Session,
        version_tag: str,
        weights_path: str,
        metadata_path: Optional[str] = None,
        accuracy: Optional[float] = None,
        macro_f1: Optional[float] = None
    ) -> ModelVersion:
        existing = db.query(ModelVersion).filter(ModelVersion.version_tag == version_tag).first()
        if existing:
            existing.weights_path = weights_path
            existing.metadata_path = metadata_path
            existing.accuracy = accuracy
            existing.macro_f1 = macro_f1
            db.commit()
            db.refresh(existing)
            return existing

        model_ver = ModelVersion(
            version_tag=version_tag,
            architecture="MobileNetV3-Small",
            weights_path=weights_path,
            metadata_path=metadata_path,
            accuracy=accuracy,
            macro_f1=macro_f1,
            is_active=False,
            is_promoted=False
        )
        db.add(model_ver)
        db.commit()
        db.refresh(model_ver)
        return model_ver

    @staticmethod
    def promote_model(db: Session, version_tag: str) -> ModelVersion:
        """
        Promotes candidate model to active production status
        ONLY if it exists and has passed evaluation criteria.
        """
        target = db.query(ModelVersion).filter(ModelVersion.version_tag == version_tag).first()
        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model version '{version_tag}' not found in registry."
            )

        # Check weights file existence
        if not Path(target.weights_path).exists():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Model weights file '{target.weights_path}' does not exist on disk."
            )

        # Check evaluation requirements
        latest_eval = db.query(ModelEvaluation).filter(
            ModelEvaluation.model_version_tag == version_tag
        ).order_by(ModelEvaluation.evaluated_at.desc()).first()

        if not latest_eval or not latest_eval.passed_threshold:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot promote model '{version_tag}': Candidate has not passed quality evaluation criteria."
            )

        # Deactivate previous active models
        db.query(ModelVersion).filter(ModelVersion.is_active == True).update({"is_active": False})
        
        # Promote target
        target.is_active = True
        target.is_promoted = True
        target.promoted_at = utc_now()
        db.commit()
        db.refresh(target)

        # Reload inference service
        InferenceService.get_instance().load_model(target.version_tag)
        logger.info(f"Model version '{version_tag}' promoted to active production model.")
        return target
