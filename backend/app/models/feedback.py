import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db.base import Base, utc_now

class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    room_id = Column(String(36), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    layout_id = Column(String(36), ForeignKey("layouts.id", ondelete="SET NULL"), nullable=True, index=True)
    furniture_id = Column(String(36), ForeignKey("furniture_items.id", ondelete="SET NULL"), nullable=True)
    model_version = Column(String(50), nullable=False, index=True)
    
    # Satisfaction ratings
    is_liked = Column(Boolean, nullable=True)
    star_rating = Column(Integer, nullable=True)  # 1 to 5
    accepted_recommendation = Column(Boolean, default=True, nullable=False)
    
    # Ground-truth correction & training validation
    corrected_room_type = Column(String(50), nullable=True, index=True)
    is_approved_for_training = Column(Boolean, default=False, nullable=False)
    approval_notes = Column(String(255), nullable=True)
    
    # Dissatisfaction & comments
    dissatisfaction_reason = Column(String(100), nullable=True)
    comments = Column(String(1000), nullable=True)
    
    # Layout adjustments recorded from 3D canvas
    user_adjusted_layout = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=utc_now, nullable=False)

    room = relationship("Room", back_populates="feedbacks")
    layout = relationship("Layout", back_populates="feedbacks")
