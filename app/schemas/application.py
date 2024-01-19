# app/schemas/application.py
from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime
from .user import UserPublic
from .job import JobPublic

class ApplicationBase(BaseModel):
    cover_letter: constr(min_length=20)

class ApplicationCreate(ApplicationBase):
    job_id: int

class ApplicationUpdate(BaseModel):
    cover_letter: Optional[constr(min_length=20)] = None
    status: Optional[str] = None

class ApplicationInDBBase(ApplicationBase):
    id: int
    status: str
    applied_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Application(ApplicationInDBBase):
    applicant: UserPublic
    job: JobPublic

class ApplicationPublic(ApplicationInDBBase):
    # This schema is for public representation, possibly excluding sensitive details
    pass
