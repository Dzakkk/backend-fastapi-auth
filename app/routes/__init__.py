from fastapi import APIRouter
from .user_route import UserRouter

main_router = APIRouter()

main_router.include_router(router=UserRouter, tags=["user Routes"])
