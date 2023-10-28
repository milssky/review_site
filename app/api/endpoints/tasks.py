from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import tasks_crud

router = APIRouter()


@router.get("/")
async def get_user_tasks():
    pass


@router.get("/{task_id}")
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    task = await tasks_crud.get(
        session=session,
        id=task_id,
    )
    return task


@router.post("/")
async def create_task():
    pass
