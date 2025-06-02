from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
import datetime  # Changed import


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


class TypeTrainingBase(BaseModel):
    name: Optional[str] = None


class TypeTrainingCreate(TypeTrainingBase):
    name: str


class TypeTrainingUpdate(TypeTrainingBase):
    pass


class TypeTraining(TypeTrainingBase):
    id: int

    class Config:
        orm_mode = True


# Schemas for ObjetivesDay
class ObjetivesDayBase(BaseModel):
    date: Optional[datetime.date] = None  # Prefixed with module
    obj_calories: Optional[int] = None
    obj_steps: Optional[int] = None
    obj_moviment: Optional[int] = None
    obj_dream: Optional[float] = None
    id_user_create: Optional[int] = None
    id_user_update: Optional[int] = None


class ObjetivesDayCreate(ObjetivesDayBase):
    date: datetime.date  # Prefixed with module
    id_user_create: int


class ObjetivesDayUpdate(ObjetivesDayBase):
    pass


class ObjetivesDay(ObjetivesDayBase):
    id: int
    create_date: Optional[datetime.datetime] = None  # Prefixed with module
    update_date: Optional[datetime.datetime] = None  # Prefixed with module

    class Config:
        orm_mode = True
