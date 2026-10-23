from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.schemas.feedback import (
    UserFeedbackCreate,
    UserFeedbackResponse,
    FeedbackSummaryResponse,
    FeedbackApproveRequest
)
from backend.app.services.feedback_service import FeedbackService
from backend.app.core.security import verify_admin_api_key

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("", response_model=UserFeedbackResponse, status_code=status.HTTP_201_CREATED)
def submit_feedback(payload: UserFeedbackCreate, db: Session = Depends(get_db)):
    return FeedbackService.create_feedback(db, payload)

@router.get("", response_model=List[UserFeedbackResponse])
def get_feedbacks(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    return FeedbackService.get_all(db, skip=skip, limit=limit)

@router.get("/summary", response_model=FeedbackSummaryResponse)
def get_feedback_summary(db: Session = Depends(get_db)):
    return FeedbackService.get_summary(db)

@router.post("/{feedback_id}/approve", response_model=UserFeedbackResponse)
def approve_feedback_for_retraining(
    feedback_id: str,
    payload: FeedbackApproveRequest,
    db: Session = Depends(get_db),
    _authorized: bool = Depends(verify_admin_api_key)
):
    return FeedbackService.approve_feedback_for_training(
        db=db,
        feedback_id=feedback_id,
        is_approved=payload.is_approved_for_training,
        notes=payload.approval_notes
    )
