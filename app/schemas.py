from pydantic import BaseModel, EmailStr
from datetime import date
from uuid import UUID

class UserCreate(BaseModel):
    email:EmailStr
    password:str
    
class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class LearningEntryCreate(BaseModel):
    date:date
    hours:float
    topic:str
    notes:str | None = None
    
class LearningEntryResponse(BaseModel):
    id:UUID
    date:date
    hours:float
    topic:str
    notes:str | None
    
    class Config:
        from_attributes = True
    