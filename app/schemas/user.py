from typing import Optional

from fastapi_users import schemas


# TODO: Избавится от дублирования полей
class UserRead(schemas.BaseUser[int]):
    username: str
    first_name: str
    last_name: str
    is_teacher: bool


class UserCreate(schemas.BaseUserCreate):
    username: str
    first_name: str
    last_name: str
    is_teacher: bool = False


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_teacher: Optional[bool] = None