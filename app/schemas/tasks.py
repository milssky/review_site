from pydantic import BaseModel


class TaskDB(BaseModel):
    name: str
    text: str
    language: list[str]
