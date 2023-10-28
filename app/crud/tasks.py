from app.crud.base import CRUDBase
from app.models.task import Task


class TasksCRUD(CRUDBase[Task]):
    pass


tasks_crud = TasksCRUD(Task)
