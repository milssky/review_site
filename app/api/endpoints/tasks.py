from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import validator
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import tasks_crud
from app.models.user import User
from app.schemas import TaskCreate, TaskDB, UserTask

router = APIRouter()


@router.get(
    "/",
)
async def get_user_tasks(
    user: User = Depends(current_user),
    sesson: AsyncSession = Depends(get_async_session),
) -> list[UserTask]:
    """Возвращает задачи текущего пользователя."""
    tasks = await tasks_crud.get_user_tasks(
        user_id=user.id,
        session=sesson,
    )
    print(dir(tasks[0]))
    return tasks  # type: ignore


@router.post(
    "/",
)
async def create_task(
    task_data: TaskCreate,
    user: User = Depends(current_superuser),
    session: AsyncSession = Depends(get_async_session),
) -> TaskDB:
    """Создает задачу. Доступно только преподавателю."""
    task, created = await tasks_crud.get_or_create(
        **task_data.model_dump(),
        session=session,
    )
    return task


@router.post(
    "/{task_id}/{user_id}",
)
async def give_task(
    task_id: int,
    user_id: int,
    user: User = Depends(current_superuser),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    """Присвоить задачу пользователю."""

    await tasks_crud.give_user_tasks(
        user_id=user_id,
        task_id=task_id,
        session=session,
    )


@router.get(
    "/{task_id}",
)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> TaskDB:
    task = await tasks_crud.get(
        session=session,
        id=task_id,
    )
    return task


@router.delete(
    "/{task_id}",
    status_code=204,
)
@validator(name="is_task_author")
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> None:
    await tasks_crud.delete(
        session=session,
        id=task_id,
    )
