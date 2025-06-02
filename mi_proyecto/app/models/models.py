from sqlalchemy import (
    Column, Integer, String, Enum, Date, Float, DateTime
)  # Added Date, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func  # Added func for CURRENT_TIMESTAMP

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    user_name = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    password = Column(String(255), nullable=True)  # Increased to 255 for longer hashes
    state = Column(Enum('0', '1', '2', '3'), nullable=False)


class TypeTraining(Base):
    __tablename__ = "type_training"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=True)


class ObjetivesDay(Base):
    __tablename__ = "objetives_day"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, nullable=True)
    obj_calories = Column(Integer, nullable=True)
    obj_steps = Column(Integer, nullable=True)
    obj_moviment = Column(Integer, nullable=True)
    obj_dream = Column(Float(5, 2), nullable=True)
    id_user_create = Column(Integer, nullable=True)
    create_date = Column(DateTime, server_default=func.now(), nullable=True)
    id_user_update = Column(Integer, nullable=True)
    update_date = Column(DateTime, server_default=func.now(),
                       onupdate=func.now(), nullable=True)