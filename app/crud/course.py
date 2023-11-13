from app.crud.base import CRUDBase
from app.models import Course


class CourseCRUD(CRUDBase[Course]):
    pass


course_crud = CourseCRUD(Course)
