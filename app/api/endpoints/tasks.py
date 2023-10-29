from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import validator
from app.core.db import get_async_session
from app.crud import tasks_crud
from app.schemas.tasks import TaskGet

router = APIRouter()


@router.get(
    "/",
)
async def get_user_tasks():
    pass


@router.get(
    "/{task_id}",
)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> TaskGet:
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


@router.post(
    "/",
)
async def create_task():
    pass
