from typing import Generic, Sequence, Type, TypeVar

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
        self,
        session: AsyncSession,
        **kwargs,
    ) -> ModelType | None:
        instance = await session.execute(select(self).filter_by(**kwargs))
        return instance.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession,
        **kwargs,
    ) -> Sequence[ModelType]:
        instances = await session.execute(select(self.model).filter_by(**kwargs))
        return instances.scalars().all()

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession,
    ) -> ModelType | None:
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(select(self.model).where(attr == attr_value))
        return db_obj.scalars().first()

    async def get_or_create(
        self,
        session: AsyncSession,
        **kwargs,
    ):
        instance = await session.execute(select(self).filter_by(**kwargs))
        instance = instance.scalars().first()

        if not instance:
            instance = await session.execute(insert(self.model).values(**kwargs))
            await session.commit()
        return instance

    async def update(
        self,
        obj: ModelType,
        session: AsyncSession,
        **kwargs,
    ) -> ModelType:
        await session.execute(update(obj).values(**kwargs))
        await session.refresh(obj)
        return obj

    async def delete(
        self,
        session: AsyncSession,
        *args,
        **kwargs,
    ) -> None:
        if args:
            instance = await session.execute(select(self.model).where(*args))
        else:
            instance = await session.execute(select(self.model).filter_by(**kwargs))

        await session.delete(instance)
        await session.commit()
