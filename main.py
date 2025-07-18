from fastapi import FastAPI, Depends, Query, HTTPException
from sqlmodel import Field, SQLModel, create_engine, Session, select
from typing import Annotated
from enum import Enum
import os
from dotenv import load_dotenv

load_dotenv()

db_username = os.getenv("USER_DB")
db_password = os.getenv("PASSWORD_DB")
db_host = os.getenv("HOST_DB")
db_name = os.getenv("NAME_DB")

DATABASE_URL = f'mysql+pymysql://{db_username}:{db_password}@{db_host}:3306/{db_name}'
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

session_dep = Annotated[Session, Depends(get_session)]

class UserState(str, Enum):
    NEW = "0"
    ACTIVE = "1"
    SUSPENDED = "2"
    DELETED = "3"

class Users(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, description="Nombre del usuario")
    user_name: str = Field(max_length=20, description="Nombre de usuario único", unique=True)
    email: str = Field(max_length=100, description="Correo electrónico del usuario", unique=True)
    password: str = Field(max_length=64, description="Contraseña del usuario")
    state: str = Field(default=UserState.NEW, max_length=1, description="Estado del usuario")

class UsersBase(SQLModel):
    name: str = Field(max_length=50, description="Nombre del usuario")
    user_name: str = Field(max_length=20, description="Nombre de usuario único")
    email: str = Field(max_length=100, description="Correo electrónico del usuario")
    
class UsersCreate(UsersBase):
    password: str = Field(max_length=64, description="Contraseña del usuario")
    state: UserState = Field(default=UserState.NEW, description="Estado del usuario")
    
class UsersRead(UsersBase):
    id: int = Field(description="ID del usuario")
    state: UserState
    
class UsersUpdate(UsersBase):
    name: str | None = Field(default=None, max_length=50, description="Nombre del usuario")
    user_name: str | None = Field(default=None, max_length=20, description="Nombre de usuario único")
    email: str | None = Field(default=None, max_length=100, description="Correo electrónico del usuario")
    password: str | None = Field(default=None, max_length=64, description="Contraseña del usuario")
    state: UserState | None = Field(default=None, description="Estado del usuario")

    
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to My Fitness Backend!"}

@app.post("/users/", response_model=UsersRead)
def create_user(user: UsersCreate, session: session_dep):
    user_data = user.model_dump()
    db_user = Users(**user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[UsersRead])
def read_users(
    session: session_dep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    ):
    users = session.exec(select(Users).offset(offset).limit(limit)).all()
    return users

@app.get("/users/{user_id}", response_model=UsersRead)
def read_user(user_id: int, session: session_dep):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/users/{user_id}", response_model=UsersRead)
def update_user(user_id: int, user: UsersUpdate, session: session_dep):
    user_db = session.get(Users, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db

@app.delete("/users/{user_id}")
def delete_user(user_id: int, session: session_dep):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}

