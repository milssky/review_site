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
    ) -> list[UserTask]:
        instances = await session.execute(
            select(self.model)
            .join(UserTask, UserTask.user_id == user_id)
            .options(
                selectinload(self.model.course),
                selectinload(self.model.solutions),
            )
            .add_columns(UserTask.is_solved)
        )
        return [
            {**row[0].__dict__, "is_solved": row[1]}
            for row in instances.all()  # type:ignore
        ]

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
