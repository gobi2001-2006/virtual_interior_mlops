from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TopPrediction(BaseModel):
    class_name: str
    confidence: float

class RoomPredictResponse(BaseModel):
    model_version: str
    predicted_room: str
    confidence: float
    probabilities: Dict[str, float]
    latency_ms: Optional[float] = None
    is_demo_fallback: Optional[bool] = False

class ModelStatusResponse(BaseModel):
    model_version: str
    is_loaded: bool
    is_trained: bool
    device: str
    architecture: str
    classes: List[str]
    num_classes: int

class RoomPredictionResponse(BaseModel):
    id: str
    room_id: str
    model_version: str
    predicted_room_type: str
    confidence: float
    top_predictions: List[TopPrediction]
    is_demo_fallback: bool
    latency_ms: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RoomCreate(BaseModel):
    name: Optional[str] = "My Room"
    room_type_preference: Optional[str] = None
    style_preference: Optional[str] = "modern"
    budget_preference: Optional[str] = "medium"
    width_m: Optional[float] = 4.0
    length_m: Optional[float] = 5.0
    height_m: Optional[float] = 2.8

class RoomUpdate(BaseModel):
    name: Optional[str] = None
    room_type_preference: Optional[str] = None
    style_preference: Optional[str] = None
    budget_preference: Optional[str] = None
    width_m: Optional[float] = None
    length_m: Optional[float] = None
    height_m: Optional[float] = None

class RoomResponse(BaseModel):
    id: str
    name: str
    image_path: str
    original_filename: Optional[str]
    room_type_preference: Optional[str]
    style_preference: str
    budget_preference: str
    width_m: float
    length_m: float
    height_m: float
    created_at: datetime
    updated_at: datetime
    latest_prediction: Optional[RoomPredictionResponse] = None

    model_config = ConfigDict(from_attributes=True)
