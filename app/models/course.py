from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Course(Base):
    name = Column(String(50), unique=True)
    teacher_id = mapped_column(ForeignKey("user.id"))

    teacher: Mapped["User"] = relationship(
        back_populates="course",
        lazy="selectin",
    )
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="course",
        lazy="selectin",
    )
