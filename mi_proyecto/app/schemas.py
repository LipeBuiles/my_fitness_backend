from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class UserState(str, Enum):
    inactive = '0'
    active = '1'
    pending = '2'
    banned = '3'

class UserBase(BaseModel):
    name: Optional[str] = None
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    state: UserState

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
