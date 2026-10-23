import uuid
from sqlalchemy import Column, String, Float, JSON, DateTime
from sqlalchemy.orm import relationship
from backend.app.db.base import Base, utc_now

class FurnitureItem(Base):
    __tablename__ = "furniture_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(150), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    width_m = Column(Float, nullable=False)
    height_m = Column(Float, nullable=False)
    depth_m = Column(Float, nullable=False)
    price_estimate = Column(Float, nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    style = Column(String(50), default="modern", nullable=False, index=True)
    suitable_rooms = Column(JSON, nullable=False)
    model_type = Column(String(50), default="procedural", nullable=False)
    model_path = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)
    color_hex = Column(String(20), default="#7A8B7B", nullable=False)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)

    layout_items = relationship("LayoutItem", back_populates="furniture")
