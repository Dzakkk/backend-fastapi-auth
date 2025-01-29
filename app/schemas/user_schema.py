from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid

class UserBase(BaseModel):
    username: str
    email: EmailStr
    telephone: str
    age: Optional[int]
    address: Optional[str]

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    telephone: str
    age: Optional[int]
    address: Optional[str]
    password: str

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    telephone: str
    age: Optional[int]
    address: Optional[str]

    class Config:
        orm_mode = True

class ErrorResponse(BaseModel):
    status_code: int
    detail: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserToken(BaseModel):
    access_token: str
    token_type: str = "bearer"