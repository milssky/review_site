from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models import Task, UserTask


class TasksCRUD(CRUDBase[Task]):
    async def get_user_tasks(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> list[Task]:
        instances = await session.execute(
            select(self.model, UserTask)
            .join(UserTask)
            .filter(UserTask.user_id == user_id)
            .options(
                selectinload(self.model.course),
                selectinload(self.model.solutions),
            )
        )
        return instances.scalars().all()  # type: ignore

    async def give_user_tasks(
        self,
        session: AsyncSession,
        user_id: int,
        task_id: int,
    ) -> None:
        await session.execute(
            insert(UserTask).values(
                user_id=user_id,
                task_id=task_id,
            )
        )
        await session.commit()


tasks_crud = TasksCRUD(Task)
