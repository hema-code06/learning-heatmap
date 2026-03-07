import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Float, Text, ForeignKey, DateTime, Boolean, Index, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy import relationship
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID


from .database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    estimated_hours = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    subtopics = relationship(
        "SubTopic", back_populates="topic", cascade="all, delete")
    projects = relationship(
        "Project", back_populates="topic", cascade="all, delete")


class SubTopic(Base):
    __tablename__ = "subtopics"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False
    )
    name = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    topic = relationship("Topic", back_populates="subtopics")


class Project(Base):
    __tablename__ = "projects"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    topic_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False
    )

    name = Column(String, nullable=False)

    description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    topic = relationship("Topic", back_populates="projects")


class LearningEntry(Base):
    __tablename__ = "learning_entries"

    __table_args__ = (
        Index("idx_date", "date"),
    )

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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
    badge_name = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("badge_name", "topic", name="unique_topic_badge"),
    )
