from pydantic import BaseModel
from typing import Optional
import uuid

class Attendance(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    check_in: str
    check_out: str[Optional]

class AttendanceCreate(BaseModel):
    user_id: uuid.UUID
    check_in: str

class AttendanceUpdate(BaseModel):
    check_out: str

class ErrorResponse(BaseModel):
    status_code: int
    detail: str

