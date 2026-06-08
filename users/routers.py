from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from . import crud, schema

router = APIRouter()

@router.post("/", response_model=schema.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return crud.create_user(db=db, user=user)

@router.post("/bulk", response_model=list[schema.UserResponse], status_code=status.HTTP_201_CREATED)
def create_bulk_users_endpoint(users: list[schema.UserCreate], db: Session = Depends(get_db)):
    # Check for duplicate emails in request
    emails = [u.email for u in users]
    if len(emails) != len(set(emails)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duplicate emails in the request list"
        )
    # Check if any email already exists in DB
    for email in emails:
        if crud.get_user_by_email(db, email=email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {email} is already registered"
            )
    return crud.create_list_of_users(db=db, users=users)

@router.get("/", response_model=list[schema.UserResponse])
def read_users_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schema.UserResponse)
def read_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@router.put("/{user_id}", response_model=schema.UserResponse)
def update_user_endpoint(user_id: int, user_update: schema.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user_id=user_id, user_update=user_update)

@router.delete("/{user_id}", response_model=schema.UserResponse)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user_id=user_id)
