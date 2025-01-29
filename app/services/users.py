from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.user import User
from ..schemas.user_schema import UserBase, UserResponse
from ..utils.hashing import hash_password, verify_password

class UserController:

    @staticmethod
    async def get_user(db: Session, skip: int = 0, limit: int = 10):
        user_list = db.query(User).offset(skip).limit(limit).all()
        if not user_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No User found"
            )
        return user_list
    
    @staticmethod
    async def get_user_by_name(db: Session, username: str):
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )
        return user
    
    @staticmethod
    async def create_user(input: UserBase, db: Session):
        if db.query(User).filter(User.username == input.username).first():
            raise ValueError("Username already registered")
        if db.query(User).filter(User.email == input.email).first():
            raise ValueError("Email already registered")

        hashed_password = hash_password(input.password)

        user = User(
            username=input.username,
            email=input.email,
            telephone=input.telephone,
            age=input.age,
            address=input.address,
            password=hashed_password,
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    async def update_user(db: Session, id: str, input:UserBase ):
        user = db.query(User).filter(User.id == id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )
        
        user.username = input.username
        user.email = input.email
        user.telephone = input.telephone
        user.age = input.age
        user.address = input.address

        user.password = hash_password(input.password)

        db.commit()
        db.refresh(user)
        
        return user


    @staticmethod
    async def delete_user(user_id: str, db: Session):
        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            raise ValueError("User not found")

        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}

    @staticmethod
    async def get_user_by_email(db: Session, email: str):
        user = db.query(User).filter(User.email == email).first()
        return user

    @staticmethod
    async def get_total_user(db: Session):
        total = db.query(User).count()
        return total