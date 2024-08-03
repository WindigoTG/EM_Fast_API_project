from uuid import uuid4

from sqlalchemy import Boolean, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel
from src.models import custom_types


class Step(BaseModel):
    __tablename__ = "step"

    id: Mapped[custom_types.uuid_pk_T]
    title: Mapped[custom_types.str_50_T]
    is_complete: Mapped[bool] = mapped_column(Boolean, default=False)
    task_id: Mapped[uuid4] = mapped_column(
        UUID,
        ForeignKey("task.id", ondelete="CASCADE"),
    )
    task: Mapped["Task"] = relationship(back_populates="steps")
