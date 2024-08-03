from uuid import uuid4

from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.models import BaseModel


class TaskUser(BaseModel):
    __tablename__ = "task_user"

    task_id: Mapped[uuid4] = mapped_column(
        UUID,
        ForeignKey("task.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[uuid4] = mapped_column(
        UUID,
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    )
