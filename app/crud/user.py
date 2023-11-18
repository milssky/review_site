from app.crud.base import CRUDBase
from app.models import User


class UserCRUD(CRUDBase[User]):
    pass


user_crud = UserCRUD(User)
