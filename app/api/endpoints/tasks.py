from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (validate_change_task, validate_create_task,
                                validate_exists)
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import tasks_crud, user_crud
from app.models.user import User
from app.schemas import TaskCreate, TaskDB, UserTask
from app.schemas.tasks import TaskUpdate

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
    return tasks  # type: ignore


@router.post(
    "/",
)
async def create_task(
    task_data: TaskCreate,
    _: User = Depends(current_superuser),
    session: AsyncSession = Depends(get_async_session),
) -> TaskDB:
    """Создает задачу. Доступно только преподавателю."""
    await validate_create_task(
        task_data=task_data,
        session=session,
    )

    task, created = await tasks_crud.get_or_create(
        **task_data.model_dump(),
        session=session,
    )
    return task


@router.get(
    "/{task_id}",
)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> TaskDB:
    """Получение задачи"""

    task = await tasks_crud.get(
        session=session,
        id=task_id,
    )
    return task


@router.put(
    "/{task_id}",
)
async def change_task(
    task_id: int,
    task_update: TaskUpdate,
    _: User = Depends(current_superuser),
    session: AsyncSession = Depends(get_async_session),
) -> TaskDB:
    """Изменение задачи"""

    await validate_change_task(
        task_id=task_id,
        task_data=task_update,
        session=session,
    )

    task = await tasks_crud.update(
        session=session,
        criteria=dict(id=task_id),
        **task_update.model_dump(),
    )
    return task  # type: ignore


@router.post(
    "/{task_id}/{user_id}",
)
async def give_task(
    task_id: int,
    user_id: int,
    _: User = Depends(current_superuser),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    """Присвоить задачу пользователю."""

    await validate_exists(
        row_id=task_id,
        model_name="Task",
        crud=tasks_crud,
        session=session,
    )

    await validate_exists(
        row_id=user_id,
        model_name="User",
        crud=user_crud,
        session=session,
    )

    await tasks_crud.give_user_tasks(
        user_id=user_id,
        task_id=task_id,
        session=session,
    )


@router.delete(
    "/{task_id}/{user_id}",
)
async def remove_task(
    task_id: int,
    user_id: int,
    _: User = Depends(current_superuser),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    """Удалить задачу у пользователю."""

    await validate_exists(
        row_id=task_id,
        model_name="Task",
        crud=tasks_crud,
        session=session,
    )

    await validate_exists(
        row_id=user_id,
        model_name="User",
        crud=user_crud,
        session=session,
    )

    await tasks_crud.remove_user_tasks(
        user_id=user_id,
        task_id=task_id,
        session=session,
    )


@router.delete(
    "/{task_id}",
    status_code=204,
)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> None:
    """Удалить задачу"""

    await validate_exists(
        row_id=task_id,
        model_name="Task",
        crud=tasks_crud,
        session=session,
    )

    await tasks_crud.delete(
        session=session,
        id=task_id,
    )
