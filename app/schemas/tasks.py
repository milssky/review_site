from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.course import CourseDB


class SolutionDB(BaseModel):
    task_id: int
    user_id: int
    status: bool


class GiveUserTask(BaseModel):
    task_id: int
    user_id: int


class BaseTaskSchema(BaseModel):
    name: str
    text: str
    language: list[str]


class TaskDB(BaseTaskSchema):
    solutions: list[SolutionDB]
    course: CourseDB


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    text: Optional[str] = None
    language: Optional[list[str]] = None
    course_id: Optional[int] = None


class UserTask(TaskDB):
    is_solved: bool


class TaskCreate(BaseTaskSchema):
    course_id: int


# Solutions


class File(BaseModel):
    name: str
    content: str


class SolutionTask(BaseTaskSchema):
    course: CourseDB


class SolutionGet(BaseModel):
    status: bool
    files: list[File]
    task: SolutionTask
    solved_date: datetime
