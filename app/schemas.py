from pydantic import BaseModel, EmailStr, Field
from datetime import date as DateType
from typing import Optional
from uuid import UUID


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class LearningEntryBase(BaseModel):
    date: DateType
    hours: float
    topic: str

    purpose: PurposeOfSession
    project: ProjectSection


class LearningEntryCreate(LearningEntryBase):
    pass


class LearningEntryUpdate(BaseModel):
    date: Optional[DateType] = None
    hours: Optional[float] = None
    topic: Optional[str] = None
    purpose: Optional[PurposeOfSession] = None
    project: Optional[ProjectSection] = None


class LearningEntryResponse(LearningEntryBase):
    id: UUID

    class Config:
        from_attributes = True


class PurposeOfSession(BaseModel):
    clarity_goal: str = Field(..., min_length=5)
    practical_goal: str = Field(..., min_length=5)
    problem_target: str = Field(..., min_length=5)
    skill_focus: str = Field(..., min_length=3)
    success_criteria: str = Field(..., min_length=5)


class ProjectSection(BaseModel):
    project_name: str = Field(..., min_length=3)
    project_purpose: str = Field(..., min_length=5)
    implementation_summary: str = Field(..., min_length=10)
    challenge: str = Field(..., min_length=5)
    solution: str = Field(..., min_length=5)
    self_review: str = Field(..., min_length=5)
