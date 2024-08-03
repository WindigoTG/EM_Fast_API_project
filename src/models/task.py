from typing import List, Optional
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Enum, ForeignKey, UUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel
from src.models import custom_types
from src.tasks.utils.enums import TaskStatusEnum


class Task(BaseModel):
    __tablename__ = "task"

    id: Mapped[custom_types.uuid_pk_T]
    title: Mapped[custom_types.str_50_T]
    description: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=None,
    )
    deadline: Mapped[datetime]
    status: Mapped[Enum] = mapped_column(
        Enum(TaskStatusEnum),
        default=TaskStatusEnum.pending,
    )

    author_id: Mapped[uuid4] = mapped_column(
        UUID,
        ForeignKey("user.id"),
    )
    author: Mapped["User"] = relationship(back_populates="created_tasks")
    approver_id_id: Mapped[Optional[uuid4]] = mapped_column(
        UUID,
        ForeignKey("user.id"),
        nullable=True,
        default=None,
    )
    approver: Mapped["User"] = relationship(back_populates="approvement_tasks")
    observers: Mapped[List["User"]] = relationship(
        secondary="task_user",
        back_populates="observed_tasks"
    )
    performers: Mapped[List["User"]] = relationship(
        secondary="task_user",
        back_populates="assigned_tasks"
    )
    steps: Mapped[List["Step"]] = relationship(back_populates="task")
