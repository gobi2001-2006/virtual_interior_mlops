import io
from typing import List, Optional
from PIL import Image
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.db.session import get_db
from backend.app.models.room import Room
from backend.app.models.prediction import RoomPrediction
from backend.app.schemas.room import (
    RoomResponse,
    RoomUpdate,
    RoomPredictionResponse,
    RoomPredictResponse,
    ModelStatusResponse
)
from backend.app.services.image_service import ImageService
from backend.app.services.room_classifier_service import RoomClassifierService
from backend.app.ml.inference import InferenceService

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("/predict", response_model=RoomPredictResponse, status_code=status.HTTP_200_OK)
async def predict_room(
    file: UploadFile = File(..., description="Uploaded photograph of the room")
):
    """
    Direct model inference endpoint for room type classification using MobileNetV3-Small.
    Returns predicted room typology, confidence score, and all six class probabilities.
    """
    # 1. Validate MIME type
    if file.content_type not in settings.ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported image type '{file.content_type}'. Supported: JPEG, PNG, WebP."
        )

    # 2. Validate file size
    content = await file.read()
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Image file exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB."
        )

    # 3. Validate image integrity
    try:
        img = Image.open(io.BytesIO(content))
        img.verify()
        # Re-open after verify() because verify() clears internal buffer
        img = Image.open(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Corrupted or invalid image file: {str(e)}"
        )

    # 4. Execute inference
    inference_service = InferenceService.get_instance()
    try:
        result = inference_service.predict(img)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Inference execution failed while processing the room image."
        )

    return RoomPredictResponse(
        model_version=result["model_version"],
        predicted_room=result["predicted_room"],
        confidence=result["confidence"],
        probabilities=result["probabilities"],
        latency_ms=result.get("latency_ms"),
        is_demo_fallback=result.get("is_demo_fallback", False)
    )

@router.get("/model-status", response_model=ModelStatusResponse)
def get_model_status():
    """
    Returns the active room classification model metadata and readiness state
    without exposing sensitive filesystem paths or secrets.
    """
    inference_service = InferenceService.get_instance()
    return ModelStatusResponse(
        model_version=inference_service.loaded_version or settings.ACTIVE_MODEL_VERSION,
        is_loaded=inference_service.current_model is not None,
        is_trained=inference_service.is_trained,
        device=inference_service.device,
        architecture="MobileNetV3-Small",
        classes=inference_service.classes,
        num_classes=len(inference_service.classes)
    )

@router.post("/analyze", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def analyze_room(
    file: UploadFile = File(..., description="Uploaded photograph of the room"),
    name: str = Form("My Room"),
    room_type_preference: Optional[str] = Form(None),
    style_preference: str = Form("modern"),
    budget_preference: str = Form("medium"),
    width_m: float = Form(4.0),
    length_m: float = Form(5.0),
    height_m: float = Form(2.8),
    db: Session = Depends(get_db)
):
    # 1. Validate and save image to disk
    relative_path = await ImageService.save_upload_image(file)

    # 2. Persist room entity
    room = Room(
        name=name,
        image_path=relative_path,
        original_filename=file.filename,
        room_type_preference=room_type_preference,
        style_preference=style_preference,
        budget_preference=budget_preference,
        width_m=width_m,
        length_m=length_m,
        height_m=height_m
    )
    db.add(room)
    db.commit()
    db.refresh(room)

    # 3. Classify with genuine ML / honest demo fallback
    prediction = RoomClassifierService.classify_room_image(db, room)

    # 4. Construct response
    res = RoomResponse.model_validate(room)
    res.latest_prediction = RoomPredictionResponse.model_validate(prediction)
    return res

@router.get("", response_model=List[RoomResponse])
def get_rooms(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    rooms = db.query(Room).order_by(Room.created_at.desc()).offset(skip).limit(limit).all()
    results = []
    for r in rooms:
        res = RoomResponse.model_validate(r)
        latest_pred = db.query(RoomPrediction).filter(
            RoomPrediction.room_id == r.id
        ).order_by(RoomPrediction.created_at.desc()).first()
        if latest_pred:
            res.latest_prediction = RoomPredictionResponse.model_validate(latest_pred)
        results.append(res)
    return results

@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: str, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        
    res = RoomResponse.model_validate(room)
    latest_pred = db.query(RoomPrediction).filter(
        RoomPrediction.room_id == room.id
    ).order_by(RoomPrediction.created_at.desc()).first()
    if latest_pred:
        res.latest_prediction = RoomPredictionResponse.model_validate(latest_pred)
    return res

@router.patch("/{room_id}", response_model=RoomResponse)
def update_room(room_id: str, payload: RoomUpdate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(room, k, v)
        
    db.commit()
    db.refresh(room)
    
    res = RoomResponse.model_validate(room)
    latest_pred = db.query(RoomPrediction).filter(
        RoomPrediction.room_id == room.id
    ).order_by(RoomPrediction.created_at.desc()).first()
    if latest_pred:
        res.latest_prediction = RoomPredictionResponse.model_validate(latest_pred)
    return res
