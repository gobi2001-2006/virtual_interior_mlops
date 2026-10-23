import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from backend.app.db.base import Base, utc_now

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=True)
    username = Column(String(100), unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    rooms = relationship("Room", back_populates="user", cascade="all, delete-orphan")
