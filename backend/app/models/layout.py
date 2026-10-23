import uuid
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db.base import Base, utc_now

class Layout(Base):
    __tablename__ = "layouts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    room_id = Column(String(36), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), default="Recommended Layout", nullable=False)
    room_type = Column(String(50), nullable=False)
    style = Column(String(50), default="modern", nullable=False)
    budget = Column(String(50), default="medium", nullable=False)
    total_cost = Column(Float, default=0.0, nullable=False)
    is_recommended = Column(Boolean, default=True, nullable=False)
    layout_model_version = Column(String(50), default="layout_v001", nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    room = relationship("Room", back_populates="layouts")
    items = relationship("LayoutItem", back_populates="layout", cascade="all, delete-orphan")
    feedbacks = relationship("UserFeedback", back_populates="layout", cascade="all, delete-orphan")

class LayoutItem(Base):
    __tablename__ = "layout_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    layout_id = Column(String(36), ForeignKey("layouts.id", ondelete="CASCADE"), nullable=False, index=True)
    furniture_id = Column(String(36), ForeignKey("furniture_items.id", ondelete="RESTRICT"), nullable=False, index=True)
    pos_x = Column(Float, default=0.0, nullable=False)
    pos_y = Column(Float, default=0.0, nullable=False)
    pos_z = Column(Float, default=0.0, nullable=False)
    rot_y = Column(Float, default=0.0, nullable=False)
    scale_x = Column(Float, default=1.0, nullable=False)
    scale_y = Column(Float, default=1.0, nullable=False)
    scale_z = Column(Float, default=1.0, nullable=False)
    placement_reason = Column(String(255), nullable=True)
    ml_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)

    layout = relationship("Layout", back_populates="items")
    furniture = relationship("FurnitureItem", back_populates="layout_items")
