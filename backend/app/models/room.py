import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db.base import Base, utc_now

class Room(Base):
    __tablename__ = "rooms"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    name = Column(String(100), default="My Room", nullable=False)
    image_path = Column(String(500), nullable=False)
    original_filename = Column(String(255), nullable=True)
    room_type_preference = Column(String(50), nullable=True)
    style_preference = Column(String(50), default="modern", nullable=False)
    budget_preference = Column(String(50), default="medium", nullable=False)
    width_m = Column(Float, default=4.0, nullable=False)
    length_m = Column(Float, default=5.0, nullable=False)
    height_m = Column(Float, default=2.8, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    user = relationship("User", back_populates="rooms")
    predictions = relationship("RoomPrediction", back_populates="room", cascade="all, delete-orphan")
    layouts = relationship("Layout", back_populates="room", cascade="all, delete-orphan")
    feedbacks = relationship("UserFeedback", back_populates="room", cascade="all, delete-orphan")
