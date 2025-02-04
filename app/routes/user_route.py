from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import JSONResponse
from ..schemas.user_schema import UserCreate, UserResponse, ErrorResponse, UserToken, UserLogin, UserEdit
from ..models.user import User
from fastapi.security import OAuth2PasswordBearer
from ..config.setting_session import get_db
from ..services.users import UserController
from ..utils.jwt_handler import create_access_token, verify_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..utils.hashing import verify_password

UserRouter = APIRouter()

bearer_scheme = HTTPBearer()

@UserRouter.get(path="/users", responses={404: {"model": ErrorResponse}})
async def get_users(
    page: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    try:
        skip = page * limit
        users = await UserController.get_user(db, skip, limit)
        total = await UserController.get_total_user(db)
        
        if not users: 
            raise HTTPException(status_code=404, detail="No users found")
        
        return {
            "status_code": status.HTTP_200_OK,
            "total": total,
            "data": users
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@UserRouter.get(path="/users2", responses={404: {"model": ErrorResponse}})
async def get_users(db: Session = Depends(get_db)):

    try:
        users = await UserController.get_user2(db)
        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        return {"status_code": status.HTTP_200_OK, "data": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@UserRouter.get(path="/users/{username}", responses={404: {"model": ErrorResponse}})
async def get_user_by_username(username: str, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        user = await UserController.get_user_by_name(db, username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status_code": status.HTTP_200_OK, "data": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@UserRouter.post(path="/users", responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def create_user(input: UserCreate, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        user = await UserController.create_user(input, db)
        return {"status_code": status.HTTP_201_CREATED, "data": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@UserRouter.post(path="/users2", responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def create_user(input: UserCreate, db: Session = Depends(get_db)):
    try:
        user = await UserController.create_user(input, db)
        return {"status_code": status.HTTP_201_CREATED, "data": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@UserRouter.put(path="/users/{user_id}", responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def update_user(user_id: str, input: UserEdit, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        user = await UserController.update_user(db, user_id, input)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status_code": status.HTTP_200_OK, "data": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@UserRouter.delete(path="/users/{user_id}", responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def delete_user(user_id: str, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        result = await UserController.delete_user(user_id, db)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status_code": status.HTTP_200_OK, "message": result["message"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@UserRouter.post("/login", response_model=UserToken)
async def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    user = await UserController.get_user_by_email(db, user_login.email)
    if user and verify_password(user_login.password, user.password):
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )