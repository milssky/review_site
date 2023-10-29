from pydantic import BaseModel

from app.schemas.course import CourseDB


class SolutionDB(BaseModel):
    task_id: int
    user_id: int
    status: bool


class TaskGet(BaseModel):
    name: str
    text: str
    language: list[str]
    is_solved: bool
    course: CourseDB
    solutions: list[SolutionDB]
