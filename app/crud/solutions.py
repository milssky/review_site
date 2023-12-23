from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import File, Solution


class SolutionCRUD(CRUDBase[Solution]):
    async def create_file(
        self,
        session: AsyncSession,
        solution_id: int,
        **kwargs,
    ) -> None:
        instance = File(**kwargs, solution_id=solution_id)
        session.add(instance)
        await session.commit()


solution_crud = SolutionCRUD(Solution)
