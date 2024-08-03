from typing import Optional
from uuid import uuid4

from sqlalchemy import Enum, ForeignKey, Integer, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel
from src.models.custom_types import uuid_pk_T
from src.structure.utils.enums import RoleEnum


class DivisionPosition(BaseModel):
    __tablename__ = "division_position"
    id: Mapped[uuid_pk_T]

    position_id: Mapped[uuid4] = mapped_column(
        UUID,
        ForeignKey("position.id", ondelete="CASCADE"),
    )
    division_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("division.id", ondelete="CASCADE"),
    )

    position: Mapped["Position"] = relationship(
        back_populates="divisions"
    )
    division: Mapped["Division"] = relationship(
        back_populates="positions"
    )

    role: Mapped[Enum] = mapped_column(Enum(RoleEnum))

    user_id: Mapped[Optional[uuid4]] = mapped_column(
        UUID,
        ForeignKey("user.id"),
        nullable=True,
        default=None,
    )
    user: Mapped["User"] = relationship(back_populates="positions")
