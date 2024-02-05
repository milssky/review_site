from sqlalchemy import and_, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Task, UserTask


class TasksCRUD(CRUDBase[Task]):
    async def get_user_tasks(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> list[dict]:
        instances = await session.execute(
            select(self.model)
            .join(UserTask, UserTask.user_id == user_id)
            .add_columns(UserTask.is_solved)
        )
        return [{**row[0].__dict__, 'is_solved': row[1]} for row in instances.all()]

    async def get_user_task(
        self,
        user_id: int,
        task_id: int,
        session: AsyncSession,
    ):
        instance = await session.execute(
            select(UserTask).where(
                and_(
                    UserTask.user_id == user_id,
                    UserTask.task_id == task_id,
                )
            )
        )
        return instance.scalars().first()

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

    async def remove_user_tasks(
        self,
        session: AsyncSession,
        user_id: int,
        task_id: int,
    ) -> None:
        instance = await session.execute(
            select(UserTask).filter_by(
                user_id=user_id,
                task_id=task_id,
            )
        )
        instance = instance.scalars().first()
        await session.delete(instance)
        await session.commit()


tasks_crud = TasksCRUD(Task)
