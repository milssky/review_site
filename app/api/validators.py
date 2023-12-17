from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import course_crud, tasks_crud
from app.schemas.tasks import TaskCreate, TaskUpdate


async def validate_create_task(
    task_data: TaskCreate,
    session: AsyncSession,
):
    course_id = task_data.course_id
    course = await course_crud.get(
        session=session,
        id=course_id,
    )
    task = await tasks_crud.get(
        session=session,
        name=task_data.name,
    )
    errors = dict()
    if course is None:
        errors["course_id"] = "Course not found"
    if task is not None:
        errors["task_name"] = "Task with this name exist"

    if errors:
        raise HTTPException(400, detail=errors)


async def validate_change_task(
    task_data: TaskUpdate,
    task_id: int,
    session: AsyncSession,
):
    course_id = task_data.course_id
    course = await course_crud.get(
        session=session,
        id=course_id,
    )
    task = await tasks_crud.get(
        session=session,
        id=task_id,
    )
    task_duplicate_name = await tasks_crud.get(
        session=session,
        name=task_data.name,
    )
    errors = dict()
    if course is None:
        errors["course_id"] = "Course not found"
    if task is None:
        errors["task_id"] = "Task not found"
    if task_duplicate_name is not None:
        errors["task_name"] = "Task with this name exist"

    if errors:
        raise HTTPException(400, detail=errors)


async def validate_exists(
    crud,
    row_id: int,
    model_name: str,
    session: AsyncSession,
):
    instance = await crud.get(
        id=row_id,
        session=session,
    )
    if instance is None:
        raise HTTPException(
            400,
            detail={model_name: "Not found"},
        )
