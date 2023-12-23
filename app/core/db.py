from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    @declared_attr  # type: ignore
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, autoincrement=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)  # type: ignore


async def get_async_session():
    async with AsyncSessionLocal() as async_session:  # type: ignore
        yield async_session
