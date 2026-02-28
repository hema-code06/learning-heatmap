import uuid
from sqlalchemy import Column, String, Date, Float, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    learning_entries = relationship(
        "LearningEntry", back_populates="user", cascade="all, delete-orphan")


class LearningEntry(Base):
    __tablename__ = "learning_entries"

    id = Column(String, primary_key=True, default=lambda:str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False)
    hours = Column(Float, nullable=False)
    topic = Column(String, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="learning_entries")
