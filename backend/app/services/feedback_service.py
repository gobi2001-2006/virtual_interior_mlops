from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status

from backend.app.models.feedback import UserFeedback
from backend.app.schemas.feedback import UserFeedbackCreate, FeedbackSummaryResponse
from backend.app.core.logging import logger

class FeedbackService:
    @staticmethod
    def create_feedback(db: Session, payload: UserFeedbackCreate) -> UserFeedback:
        feedback = UserFeedback(**payload.model_dump())
        
        # If user provided an explicit room type correction, default approval to False
        # until verified by an authorized reviewer/admin
        if feedback.corrected_room_type:
            feedback.is_approved_for_training = False
            
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        logger.info(f"Recorded user feedback {feedback.id} for room {feedback.room_id}")
        return feedback

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 50) -> List[UserFeedback]:
        return db.query(UserFeedback).order_by(UserFeedback.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_summary(db: Session) -> FeedbackSummaryResponse:
        total = db.query(UserFeedback).count()
        if total == 0:
            return FeedbackSummaryResponse(
                total_feedbacks=0,
                positive_count=0,
                negative_count=0,
                positive_rate=0.0,
                average_star_rating=0.0,
                total_corrected_room_types=0,
                approved_for_retraining_count=0,
                dissatisfaction_reasons_breakdown={}
            )

        positives = db.query(UserFeedback).filter(
            (UserFeedback.is_liked == True) | (UserFeedback.star_rating >= 4)
        ).count()
        
        negatives = db.query(UserFeedback).filter(
            (UserFeedback.is_liked == False) | (UserFeedback.star_rating <= 2)
        ).count()
        
        avg_stars = db.query(func.avg(UserFeedback.star_rating)).filter(
            UserFeedback.star_rating.isnot(None)
        ).scalar() or 0.0
        
        corrections = db.query(UserFeedback).filter(
            UserFeedback.corrected_room_type.isnot(None)
        ).count()
        
        approved = db.query(UserFeedback).filter(
            UserFeedback.is_approved_for_training == True
        ).count()
        
        # Breakdown of dissatisfaction reasons
        reasons_query = db.query(
            UserFeedback.dissatisfaction_reason,
            func.count(UserFeedback.id)
        ).filter(
            UserFeedback.dissatisfaction_reason.isnot(None)
        ).group_by(UserFeedback.dissatisfaction_reason).all()
        
        reasons_dict = {reason: count for reason, count in reasons_query if reason}

        return FeedbackSummaryResponse(
            total_feedbacks=total,
            positive_count=positives,
            negative_count=negatives,
            positive_rate=round((positives / total) * 100.0, 1),
            average_star_rating=round(float(avg_stars), 2),
            total_corrected_room_types=corrections,
            approved_for_retraining_count=approved,
            dissatisfaction_reasons_breakdown=reasons_dict
        )

    @staticmethod
    def approve_feedback_for_training(
        db: Session,
        feedback_id: str,
        is_approved: bool,
        notes: Optional[str] = None
    ) -> UserFeedback:
        feedback = db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()
        if not feedback:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback record not found")
            
        feedback.is_approved_for_training = is_approved
        feedback.approval_notes = notes
        db.commit()
        db.refresh(feedback)
        return feedback
