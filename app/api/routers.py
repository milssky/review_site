from fastapi import APIRouter

from .endpoints import course_router, solution_router, task_router, user_router

main_router = APIRouter()
main_router.include_router(
    task_router,
    prefix='/tasks',
    tags=['Задачи'],
)
main_router.include_router(
    solution_router,
    prefix='/tasks/{task_id}/solutions',
    tags=['Решения'],
)
main_router.include_router(
    course_router,
    prefix='/course',
    tags=['Курсы'],
)

main_router.include_router(user_router)
