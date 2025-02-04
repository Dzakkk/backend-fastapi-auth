from sqlalchemy.orm import Session
from ..models.attendance import Attendance
from ..schemas.attendance_schema import AttendanceBase, AttendanceCreate, AttendanceUpdate
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
import uuid

class AttendanceController:

    @staticmethod
    async def create_attendance(input: AttendanceCreate, db: Session):
        try:
            new_attendance = Attendance(
                user_id=input.user_id,
                check_in=input.check_in,
            )
            db.add(new_attendance)
            db.commit()
            db.refresh(new_attendance)

            return new_attendance
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    @staticmethod

    async def update_attendance(db: Session, id: str, input: AttendanceUpdate):
        attendance = db.query(Attendance).filter(Attendance.id == id).first()
        if not attendance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Attendance not found"
            )
        for key, value in input.dict(exclude_unset=True).items():
            setattr(attendance, key, value)
        db.commit()
        db.refresh(attendance)
        return attendance
    
    @staticmethod
    async def delete_attendance(attendance_id: str, db: Session):
        attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
        if not attendance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Attendance not found"
            )
        db.delete(attendance)
        db.commit()
        return {"message": "Attendance deleted successfully"}
    
    @staticmethod
    async def get_attendance(db: Session, skip: int = 0, limit: int = 10):
        attendance_list = db.query(Attendance).offset(skip).limit(limit).all()
        if not attendance_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No Attendance found"
            )
        return attendance_list
    
    @staticmethod
    async def get_attendance_by_id(db: Session, attendance_id: str):
        attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
        if not attendance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Attendance not found"
            )
        return attendance
    
    @staticmethod
    async def get_attendance_by_user_id(db: Session, user_id: str):
        attendance = db.query(Attendance).filter(Attendance.user_id == user_id).all()
        return attendance if attendance else []