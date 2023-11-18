import json

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, String, Table,
                        TypeDecorator)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.db import Base


class ArrayType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)


class Task(Base):
    name = Column(String(50), unique=True)
    text = Column(String(1000))
    language = Column(ArrayType(100))
    course_id = mapped_column(ForeignKey("course.id"))

    course: Mapped["Course"] = relationship(
        back_populates="tasks",
        lazy="selectin",
    )
    solutions: Mapped[list["Solution"]] = relationship(
        back_populates="task",
        lazy="selectin",
    )


class Solution(Base):
    author_id = mapped_column(ForeignKey("user.id"))
    task_id = mapped_column(ForeignKey("task.id"))
    solved_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Boolean(), default=False)

    task: Mapped["Task"] = relationship(
        back_populates="solutions",
        lazy="selectin",
    )
    author: Mapped["User"] = relationship(
        back_populates="solutions",
        lazy="selectin",
    )
    files: Mapped[list["File"]] = relationship(
        back_populates="solution",
        lazy="selectin",
    )


class File(Base):
    name = Column(String(500))
    content = Column(String(1000))
    solution_id = mapped_column(ForeignKey("solution.id"))

    solution: Mapped["Solution"] = relationship(
        back_populates="files",
        lazy="selectin",
    )


UserSolutions = Table(
    "usersolutions",
    Base.metadata,
    Column("task_id", ForeignKey("task.id")),
    Column("user_id", ForeignKey("user.id")),
    Column("solution_id", ForeignKey("solution.id")),
)


class UserTask(Base):
    task_id = mapped_column(ForeignKey("task.id"))
    user_id = mapped_column(ForeignKey("user.id"))
    is_solved = Column(Boolean(), default=False)
