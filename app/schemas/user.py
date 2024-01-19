# app/schemas/user.py
from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: constr(min_length=6)

class UserUpdate(BaseModel):
    username: Optional[constr(min_length=3, max_length=50)] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_hr: Optional[bool] = None

class UserInDBBase(UserBase):
    id: int
    is_active: bool
    is_hr: bool

    class Config:
        orm_mode = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

class UserPublic(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
