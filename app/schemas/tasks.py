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


class UserTask(TaskDB):
    is_solved: bool


class TaskCreate(BaseTaskSchema):
    course_id: int
