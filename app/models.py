import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Float, Text, ForeignKey, DateTime, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID


from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    learning_entries = relationship(
        "LearningEntry", back_populates="user", cascade="all, delete-orphan"
    )
    goals = relationship(
        "MonthlyGoal", back_populates="user", cascade="all, delete-orphan"
    )


class LearningEntry(Base):
    __tablename__ = "learning_entries"

    __table_args__ = (
        Index("idx_user_date", "user_id", "date"),
    )

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey(
        "users.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False)
    hours = Column(Float, nullable=False)
    topic = Column(String, nullable=False)
    
    # Purpose of Session (Required)
    clarity_goal = Column(Text, nullable=False)
    practical_goal = Column(Text, nullable=False)
    problem_target = Column(Text, nullable=False)
    skill_focus = Column(Text, nullable=False)
    success_criteria = Column(Text, nullable=False)
    
    # Project Section (Required)
    project_name = Column(Text, nullable=False)
    project_purpose = Column(Text, nullable=False)
    implementation_summary = Column(Text, nullable=False)
    challenge = Column(Text, nullable=False)
    solution = Column(Text, nullable=False)
    self_review = Column(Text, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="learning_entries")


class MonthlyGoal(Base):
    __tablename__ = "monthly_goals"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey(
        "users.id", ondelete="CASCADE"))
    month = Column(String, nullable=False)
    target_hours = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="goals")


class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    badge_name = Column(String, nullable=False)
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    __table_args__ = (
        UniqueConstraint("user_id", "badge_name", name="unique_user_badge"),
    )
