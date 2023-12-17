from fastapi import APIRouter, Depends, HTTPException
from fastapi.datastructures import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import validate_exists
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud import solution_crud, tasks_crud
from app.models.user import User
from app.schemas.tasks import SolutionGet
from app.services import extract

router = APIRouter()


@router.post(
    '/',
)
async def create_solution(
    task_id: int,
    file: UploadFile,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Создает решение"""

    if file.filename is None:
        raise HTTPException(
            400,
            detail={'file_name': 'filename not found'},
        )
    solution, _ = await solution_crud.get_or_create(
        session=session,
        author_id=user.id,
        task_id=task_id,
    )
    await extract(
        file=file,
        solution_id=solution.id,
    )
    return {'status': 'Файлы решения были получены'}


@router.get(
    '/{solution_id}',
)
async def get_solution(
    task_id: int,
    solution_id: int,
    _: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> SolutionGet:
    await validate_exists(
        row_id=task_id,
        model_name='Task',
        crud=tasks_crud,
        session=session,
    )

    await validate_exists(
        row_id=solution_id,
        model_name='Solution',
        crud=solution_crud,
        session=session,
    )

    solution = await solution_crud.get(
        task_id=task_id,
        id=solution_id,
        session=session,
    )
    return solution
