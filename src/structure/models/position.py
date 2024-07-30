from typing import List

from sqlalchemy.orm import Mapped, relationship

from src.models import BaseModel, custom_types


class Position(BaseModel):
    __tablename__ = "position"

    id: Mapped[custom_types.uuid_pk_T]
    title: Mapped[custom_types.str_50_T]

    divisions: Mapped[List["DivisionPosition"]] = relationship(
        back_populates="position"
    )
