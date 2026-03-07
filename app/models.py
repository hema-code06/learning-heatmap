import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Float, DateTime, Index, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PGUUID


from .database import Base


class LearningEntry(Base):
    __tablename__ = "learning_entries"

    __table_args__ = (
        Index("idx_user_date", "user_id", "date"),
    )

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(Integer, default=1)

    date = Column(Date, nullable=False)
    hours = Column(Float, nullable=False)
    topic = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MonthlyGoal(Base):
    __tablename__ = "monthly_goals"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, default=1)

    month = Column(String, nullable=False)
    target_hours = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, default=1)

    badge_name = Column(String, nullable=False)
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "badge_name", name="unique_user_badge"),
    )
