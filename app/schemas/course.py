from pydantic import BaseModel


class CourseDB(BaseModel):
    name: str
    tacher_id: int
