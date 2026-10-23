from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from backend.app.schemas.furniture import FurnitureResponse

class LayoutItemBase(BaseModel):
    furniture_id: str
    pos_x: float = Field(..., description="Meters X from room center")
    pos_y: float = Field(default=0.0, description="Meters Y (height above floor)")
    pos_z: float = Field(..., description="Meters Z from room center")
    rot_y: float = Field(default=0.0, description="Rotation around Y axis in radians")
    scale_x: float = Field(default=1.0)
    scale_y: float = Field(default=1.0)
    scale_z: float = Field(default=1.0)
    placement_reason: Optional[str] = None
    ml_score: Optional[float] = Field(default=None, description="ML suitability ranking score")

class LayoutItemCreate(LayoutItemBase):
    pass

class LayoutItemResponse(LayoutItemBase):
    id: str
    layout_id: str
    furniture: Optional[FurnitureResponse] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class LayoutCreate(BaseModel):
    room_id: str
    name: Optional[str] = "My Custom Layout"
    room_type: str
    style: Optional[str] = "modern"
    budget: Optional[str] = "medium"
    items: List[LayoutItemCreate] = []

class LayoutUpdate(BaseModel):
    name: Optional[str] = None
    items: Optional[List[LayoutItemCreate]] = None

class LayoutRecommendRequest(BaseModel):
    room_id: str
    room_type: Optional[str] = None
    style: Optional[str] = "modern"
    budget: Optional[str] = "medium"
    width_m: Optional[float] = None
    length_m: Optional[float] = None
    height_m: Optional[float] = None

class LayoutWarning(BaseModel):
    code: str
    message: str

class LayoutResponse(BaseModel):
    id: str
    room_id: str
    name: str
    room_type: str
    style: str
    budget: str
    total_cost: float
    is_recommended: bool
    layout_model_version: Optional[str] = "layout_v001"
    items: List[LayoutItemResponse] = []
    warnings: List[LayoutWarning] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
