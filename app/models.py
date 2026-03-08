import uuid
from sqlalchemy import Column, Integer, String, Date, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB


from .database import Base


class LearningEntry(Base):
    __tablename__ = "learning_entries"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic = Column(String, nullable=False)
    subtopics = Column(JSONB)
    from_date = Column(Date)
    to_date = Column(Date)
    hours = Column(Float, nullable=False)
    completed = Column(Boolean, default=True)
    project_name = Column(String)
    project_description = Column(Text)
    project_point1 = Column(Text)
    project_point2 = Column(Text)
    project_point3 = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MonthlyGoal(Base):
    __tablename__ = "monthly_goals"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    month = Column(String, nullable=False)
    target_hours = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic = Column(String, nullable=False)
    badge_name = Column(String, nullable=False)
    description = Column(Text)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
