from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import validate_exists
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import course_crud, user_crud
from app.models.user import User
from app.schemas import CourseDB
from app.schemas.course import CourseUpdate

router = APIRouter()


@router.get('/')
async def get_all(
    user: User = Depends(current_superuser),
    session: AsyncSession = Depends(get_async_session),
) -> list[CourseDB]:
    """Получить все доступные курсы"""

    courses = await course_crud.get_multi(session=session)
    return courses  # type: ignore


@router.post('/')
async def create(
    task_data: CourseDB,
    user: User = Depends(current_superuser),
    session: AsyncSession = Depends(get_async_session),
) -> CourseDB:
    """Создать курс."""

    course, _ = await course_crud.get_or_create(
        **task_data.model_dump(),
        session=session,
    )
    return course


@router.get(
    '/{course_id}',
)
async def get(
    course_id: int,
    user: User = Depends(current_superuser),
    session: AsyncSession = Depends(get_async_session),
) -> CourseDB:
    """Получить курс"""

    course = await course_crud.get(
        session=session,
        id=course_id,
    )
    return course


@router.put(
    '/{course_id}',
)
async def change_task(
    course_id: int,
    course_update_data: CourseUpdate,
    _: User = Depends(current_superuser),
    session: AsyncSession = Depends(get_async_session),
) -> CourseDB:
    """Изменить курс"""

    await validate_exists(
        row_id=course_id,
        model_name='Course',
        crud=course_crud,
        session=session,
    )
    if course_update_data.teacher_id:
        await validate_exists(
            row_id=course_update_data.teacher_id,
            model_name='User',
            crud=user_crud,
            session=session,
        )

    course = await course_crud.update(
        session=session,
        criteria=dict(id=course_id),
        **course_update_data.model_dump(),
    )
    return course  # type: ignore


@router.delete(
    '/{course_id}',
    status_code=204,
)
async def delete_task(
    course_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> None:
    """Удалить курс"""

    await validate_exists(
        row_id=course_id,
        model_name='Course',
        crud=course_crud,
        session=session,
    )

    await course_crud.delete(
        session=session,
        id=course_id,
    )
