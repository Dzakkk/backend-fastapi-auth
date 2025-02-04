from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import JSONResponse
from ..schemas.attendance_schema import AttendanceCreate, AttendanceUpdate, ErrorResponse
from ..models.attendance import Attendance
from fastapi.security import OAuth2PasswordBearer
from ..config.setting_session import get_db
from ..services.attendance import AttendanceController
from ..utils.jwt_handler import create_access_token, verify_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..utils.hashing import verify_password

AttendanceRouter = APIRouter()

bearer_scheme = HTTPBearer()

@AttendanceRouter.post(path="/attendances", responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def create_attendance(input: AttendanceCreate, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        attendance = await AttendanceController.create_attendance(input, db)
        return {"status_code": status.HTTP_201_CREATED, "data": attendance}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@AttendanceRouter.get(path="/attendances", responses={404: {"model": ErrorResponse}})
async def get_attendances(db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        attendances = await AttendanceController.get_attendance(db)
        if not attendances:
            raise HTTPException(status_code=404, detail="No Attendance found")
        return {"status_code": status.HTTP_200_OK, "data": attendances}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@AttendanceRouter.put(path="/attendances/{attendance_id}", responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def update_attendance(attendance_id: str, input: AttendanceUpdate, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        attendance = await AttendanceController.update_attendance(db, attendance_id, input)
        if not attendance:
            raise HTTPException(status_code=404, detail="Attendance not found")
        return {"status_code": status.HTTP_200_OK, "data": attendance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@AttendanceRouter.delete(path="/attendances/{attendance_id}", responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def delete_attendance(attendance_id: str, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        result = await AttendanceController.delete_attendance(attendance_id, db)
        if not result:
            raise HTTPException(status_code=404, detail="Attendance not found")
        return {"status_code": status.HTTP_200_OK, "message": result["message"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@AttendanceRouter.get(path="/attendances/{user_id}", responses={404: {"model": ErrorResponse}})
async def get_attendances_by_user_id(user_id: str, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        attendances = await AttendanceController.get_attendance_by_user_id(db, user_id)
        if not attendances:
            raise HTTPException(status_code=404, detail="No Attendance found")
        return {"status_code": status.HTTP_200_OK, "data": attendances}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))