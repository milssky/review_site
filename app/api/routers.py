from fastapi import APIRouter

from .endpoints import task_router

main_router = APIRouter()
main_router.include_router(
    task_router,
    prefix="/tasks",
    tags=["Tasks"],
)
