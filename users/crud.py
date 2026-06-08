from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from .models import User
from .schema import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate):
    db_user = User(
        id=user.id,
        email=user.email,
        hashed_password=user.password,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_list_of_users(db: Session, users: list[UserCreate]):
    db_users = []
    for user in users:
        db_user = User(
            id=user.id,
            email=user.email,
            hashed_password=user.password,
            is_active=user.is_active
        )
        db.add(db_user)
        db_users.append(db_user)
    db.commit()
    for db_user in db_users:
        db.refresh(db_user)
    return db_users


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "password":
            db_user.hashed_password = value
        else:
            setattr(db_user, key, value)
            
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(db_user)
    db.commit()
    return db_user