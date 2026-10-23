import os
from pathlib import Path
from PIL import Image
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.models.room import Room
from backend.app.models.prediction import RoomPrediction
from backend.app.models.mlops import PredictionEvent
from backend.app.ml.inference import InferenceService

class RoomClassifierService:
    @staticmethod
    def classify_room_image(db: Session, room: Room) -> RoomPrediction:
        # Resolve disk path
        clean_rel = room.image_path.lstrip("/").replace("uploads/", "")
        disk_path = Path(settings.UPLOAD_DIR) / clean_rel
        
        if not disk_path.exists():
            # Try direct relative path
            disk_path = Path(settings.BASE_DIR) / room.image_path.lstrip("/")
            
        if not disk_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Image file for room {room.id} not found on disk."
            )

        try:
            pil_img = Image.open(disk_path)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to read image file: {e}"
            )

        inference_service = InferenceService.get_instance()
        result = inference_service.predict(pil_img)

        prediction = RoomPrediction(
            room_id=room.id,
            model_version=result["model_version"],
            predicted_room_type=result["predicted_room_type"],
            confidence=result["confidence"],
            top_predictions=result["top_predictions"],
            is_demo_fallback=result["is_demo_fallback"],
            latency_ms=result["latency_ms"]
        )
        db.add(prediction)

        # Log MLOps prediction event
        event = PredictionEvent(
            model_version=result["model_version"],
            predicted_room_type=result["predicted_room_type"],
            confidence=result["confidence"],
            latency_ms=result["latency_ms"],
            is_demo_fallback=result["is_demo_fallback"]
        )
        db.add(event)
        
        db.commit()
        db.refresh(prediction)
        return prediction
