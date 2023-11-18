from fastapi import APIRouter

from .endpoints import task_router, user_router

main_router = APIRouter()
main_router.include_router(
    task_router,
    prefix="/tasks",
    tags=["Tasks"],
)
main_router.include_router(user_router)
