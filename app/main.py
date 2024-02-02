from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_first_superuser()
    yield


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    lifespan=lifespan,
)

app.include_router(main_router)
