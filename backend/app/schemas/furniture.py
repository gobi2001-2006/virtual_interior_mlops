from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class FurnitureCreate(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Nordic Comfort 3-Seater Sofa"})
    category: str = Field(..., json_schema_extra={"example": "Sofa"})
    width_m: float = Field(..., json_schema_extra={"example": 2.1})
    height_m: float = Field(..., json_schema_extra={"example": 0.85})
    depth_m: float = Field(..., json_schema_extra={"example": 0.9})
    price_estimate: float = Field(..., json_schema_extra={"example": 550.0})
    currency: str = Field(default="USD")
    style: str = Field(default="modern", json_schema_extra={"example": "Scandinavian"})
    suitable_rooms: List[str] = Field(..., json_schema_extra={"example": ["LivingRoom"]})
    model_type: str = Field(default="procedural")
    model_path: Optional[str] = None
    image_url: Optional[str] = None
    color_hex: str = Field(default="#5A6D5D")
    description: Optional[str] = None

class FurnitureResponse(BaseModel):
    id: str
    name: str
    category: str
    width_m: float
    height_m: float
    depth_m: float
    price_estimate: float
    currency: str
    style: str
    suitable_rooms: List[str]
    model_type: str
    model_path: Optional[str]
    image_url: Optional[str] = None
    color_hex: str
    description: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FurnitureFilter(BaseModel):
    category: Optional[str] = None
    room_type: Optional[str] = None
    style: Optional[str] = None
    max_price: Optional[float] = None
