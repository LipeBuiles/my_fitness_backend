from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import bcrypt

from ..models.models import User as UserModel
from ..models.models import TypeTraining as TypeTrainingModel
from ..models.models import ObjetivesDay as ObjetivesDayModel
from .. import schemas
from ..dependencies import get_db

router = APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_data = user.model_dump()
    # Generate a salt and hash the password with bcrypt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user_data["password"].encode('utf-8'), salt)
    user_data["password"] = hashed_password.decode('utf-8')
    
    db_user = UserModel(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)
):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user.model_dump(exclude_unset=True)
    
    # Hash the password if it's being updated
    if "password" in update_data and update_data["password"]:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(update_data["password"].encode('utf-8'), salt)
        update_data["password"] = hashed_password.decode('utf-8')
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return db_user


# Health check endpoint
@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/type-training/", response_model=schemas.TypeTraining)
def create_type_training(
    type_training: schemas.TypeTrainingCreate, db: Session = Depends(get_db)
):
    type_training_data = type_training.model_dump()
    db_type_training = TypeTrainingModel(**type_training_data)
    db.add(db_type_training)
    db.commit()
    db.refresh(db_type_training)
    return db_type_training


@router.get(
    "/type-training/",
    response_model=List[schemas.TypeTraining]
)
def read_type_trainings(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    type_trainings = db.query(TypeTrainingModel).offset(skip).limit(
        limit
    ).all()
    return type_trainings


@router.get(
    "/type-training/{type_training_id}",
    response_model=schemas.TypeTraining
)
def read_type_training(type_training_id: int, db: Session = Depends(get_db)):
    db_type_training = db.query(TypeTrainingModel).filter(
        TypeTrainingModel.id == type_training_id
    ).first()
    if db_type_training is None:
        raise HTTPException(status_code=404, detail="Type Training not found")
    return db_type_training


@router.put(
    "/type-training/{type_training_id}",
    response_model=schemas.TypeTraining
)
def update_type_training(
    type_training_id: int,
    type_training: schemas.TypeTrainingUpdate,
    db: Session = Depends(get_db)
):
    db_type_training = db.query(TypeTrainingModel).filter(
        TypeTrainingModel.id == type_training_id
    ).first()
    if db_type_training is None:
        raise HTTPException(status_code=404, detail="Type Training not found")
    
    update_data = type_training.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_type_training, key, value)
    
    db.add(db_type_training)
    db.commit()
    db.refresh(db_type_training)
    return db_type_training


@router.delete(
    "/type-training/{type_training_id}",
    response_model=schemas.TypeTraining
)
def delete_type_training(type_training_id: int, db: Session = Depends(get_db)):
    db_type_training = db.query(TypeTrainingModel).filter(
        TypeTrainingModel.id == type_training_id
    ).first()
    if db_type_training is None:
        raise HTTPException(status_code=404, detail="Type Training not found")
    
    db.delete(db_type_training)
    db.commit()
    return db_type_training


# CRUD operations for ObjetivesDay
@router.post("/objetives-day/", response_model=schemas.ObjetivesDay)
def create_objetives_day(
    objetives_day: schemas.ObjetivesDayCreate, db: Session = Depends(get_db)
):
    objetives_day_data = objetives_day.model_dump()
    db_objetives_day = ObjetivesDayModel(**objetives_day_data)
    db.add(db_objetives_day)
    db.commit()
    db.refresh(db_objetives_day)
    return db_objetives_day


@router.get("/objetives-day/", response_model=List[schemas.ObjetivesDay])
def read_objetives_days(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    objetives_days = db.query(ObjetivesDayModel).offset(skip).limit(
        limit
    ).all()
    return objetives_days


@router.get(
    "/objetives-day/{objetives_day_id}", 
    response_model=schemas.ObjetivesDay
)
def read_objetives_day(objetives_day_id: int, db: Session = Depends(get_db)):
    db_objetives_day = (
        db.query(ObjetivesDayModel)
        .filter(ObjetivesDayModel.id == objetives_day_id)
        .first()
    )
    if db_objetives_day is None:
        raise HTTPException(status_code=404, detail="ObjetivesDay not found")
    return db_objetives_day


@router.put(
    "/objetives-day/{objetives_day_id}", 
    response_model=schemas.ObjetivesDay
)
def update_objetives_day(
    objetives_day_id: int,
    objetives_day: schemas.ObjetivesDayUpdate,
    db: Session = Depends(get_db),
):
    db_objetives_day = (
        db.query(ObjetivesDayModel)
        .filter(ObjetivesDayModel.id == objetives_day_id)
        .first()
    )
    if db_objetives_day is None:
        raise HTTPException(status_code=404, detail="ObjetivesDay not found")

    update_data = objetives_day.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_objetives_day, key, value)

    db.add(db_objetives_day)
    db.commit()
    db.refresh(db_objetives_day)
    return db_objetives_day
