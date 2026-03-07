from pydantic import BaseModel, ConfigDict
from datetime import date as DateType
from typing import Optional
from uuid import UUID


class LearningEntryBase(BaseModel):
    date: DateType
    hours: float
    topic: str


class LearningEntryCreate(LearningEntryBase):
    pass


class LearningEntryUpdate(BaseModel):
    date: Optional[DateType] = None
    hours: Optional[float] = None
    topic: Optional[str] = None


class LearningEntryResponse(LearningEntryBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class TopicBase(BaseModel):
    name: str
    start_date: Optional[DateType] = None
    end_date: Optional[DateType] = None
    estimated_hours: Optional[float] = None


class TopicCreate(TopicBase):
    pass


class TopicResponse(TopicBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)


class SubTopicBase(BaseModel):
    topic_id: UUID
    name: str


class SubTopicCreate(SubTopicBase):
    pass


class SubTopicResponse(SubTopicBase):
    id: UUID
    completed: bool
    model_config = ConfigDict(from_attributes=True)


class ProjectBase(BaseModel):
    topic_id: UUID
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
