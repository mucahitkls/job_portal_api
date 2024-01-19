# app/schemas/job.py
from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime
from .user import UserPublic

class JobBase(BaseModel):
    title: constr(min_length=3, max_length=100)
    description: str
    location: str

class JobCreate(JobBase):
    employment_type: str

class JobUpdate(BaseModel):
    title: Optional[constr(min_length=3, max_length=100)] = None
    description: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    is_active: Optional[bool] = None

class JobInDBBase(JobBase):
    id: int
    employment_type: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Job(JobInDBBase):
    employer: UserPublic

class JobPublic(JobInDBBase):
    # This schema is used for public representation, excluding sensitive employer details
    pass
