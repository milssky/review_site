from typing import Generic, Type, TypeVar

from sqlalchemy import inspect, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta, Mapped, selectinload

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
    ) -> list[ModelType]:
        instances = await session.execute(select(self.model).filter_by(**kwargs))
        return instances.scalars().all()  # type: ignore

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
    ) -> tuple[ModelType, bool]:
        instance = await session.execute(
            select(self.model)
            .filter_by(**kwargs)
            .options(
                *[
                    selectinload(getattr(self.model, prop.key))
                    for prop in inspect(self.model).iterate_properties
                    if isinstance(prop, Mapped)
                ]
            )
        )
        instance = instance.scalars().first()
        create = False

        if not instance:
            create = True
            instance = self.model(**kwargs)  # type: ignore
            session.add(instance)
            await session.commit()

        return instance, create

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
