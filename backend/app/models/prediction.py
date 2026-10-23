import uuid
from sqlalchemy import Column, String, Float, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db.base import Base, utc_now

class RoomPrediction(Base):
    __tablename__ = "room_predictions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    room_id = Column(String(36), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    model_version = Column(String(50), nullable=False)
    predicted_room_type = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    top_predictions = Column(JSON, nullable=False)
    is_demo_fallback = Column(Boolean, default=False, nullable=False)
    latency_ms = Column(Float, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)

    room = relationship("Room", back_populates="predictions")
