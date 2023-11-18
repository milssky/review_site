from pydantic import BaseModel


class CourseDB(BaseModel):
    name: str
    teacher_id: int
