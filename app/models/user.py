from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    username = Column(String(50))
    is_teacher = Column(Boolean(), default=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    course: Mapped["Course"] = relationship(back_populates="teacher")
    solutions: Mapped[list["Solution"]] = relationship(back_populates="author")
