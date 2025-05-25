from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    user_name = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    password = Column(String(255), nullable=True)  # Aumentado a 255 caracteres para acomodar hashes más largos
    state = Column(Enum('0', '1', '2', '3'), nullable=False)


class TypeTraining(Base):
    __tablename__ = "type_training"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=True)