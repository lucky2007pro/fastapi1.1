from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    is_active: bool = True

class UserCreate(UserBase):
    id: Optional[int] = None
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True