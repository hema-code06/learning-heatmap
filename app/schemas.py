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

