from typing import Optional

from pydantic import BaseModel


class CourseDB(BaseModel):
    id: int
    name: str
    teacher_id: int


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    teacher_id: Optional[int] = None
