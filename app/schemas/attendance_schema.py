from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class AttendanceBase(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    check_in: datetime
    check_out: Optional[datetime] = None

class AttendanceCreate(BaseModel):
    user_id: uuid.UUID
    check_in: datetime

class AttendanceUpdate(BaseModel):
    check_out: datetime

class ErrorResponse(BaseModel):
    status_code: int
    detail: str


