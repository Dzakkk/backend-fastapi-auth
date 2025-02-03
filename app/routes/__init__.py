from fastapi import APIRouter
from .user_route import UserRouter
from .attendance_route import AttendanceRouter

main_router = APIRouter()

main_router.include_router(router=UserRouter, tags=["user Routes"])
main_router.include_router(router=AttendanceRouter, tags=["attendance Routes"])