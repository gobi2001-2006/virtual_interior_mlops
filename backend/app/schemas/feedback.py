from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class UserFeedbackCreate(BaseModel):
    room_id: str
    layout_id: Optional[str] = None
    furniture_id: Optional[str] = None
    model_version: Optional[str] = "v001"
    is_liked: Optional[bool] = None
    star_rating: Optional[int] = Field(None, ge=1, le=5)
    accepted_recommendation: bool = True
    corrected_room_type: Optional[str] = None
    dissatisfaction_reason: Optional[str] = None
    comments: Optional[str] = None
    user_adjusted_layout: Optional[Dict[str, Any]] = None

class FeedbackApproveRequest(BaseModel):
    is_approved_for_training: bool = True
    approval_notes: Optional[str] = None

class UserFeedbackResponse(BaseModel):
    id: str
    room_id: str
    layout_id: Optional[str]
    furniture_id: Optional[str]
    model_version: str
    is_liked: Optional[bool]
    star_rating: Optional[int]
    accepted_recommendation: bool
    corrected_room_type: Optional[str]
    is_approved_for_training: bool
    approval_notes: Optional[str]
    dissatisfaction_reason: Optional[str]
    comments: Optional[str]
    user_adjusted_layout: Optional[Dict[str, Any]]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FeedbackSummaryResponse(BaseModel):
    total_feedbacks: int
    positive_count: int
    negative_count: int
    positive_rate: float
    average_star_rating: float
    total_corrected_room_types: int
    approved_for_retraining_count: int
    dissatisfaction_reasons_breakdown: Dict[str, int]
