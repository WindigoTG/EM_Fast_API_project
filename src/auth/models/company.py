from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel, custom_types


class Company(BaseModel):
    __tablename__ = "company"

    id: Mapped[custom_types.uuid_pk_T]
    name: Mapped[custom_types.str_50_T]
    description: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=None,
    )
    created_at: Mapped[custom_types.created_at_T]
    updated_at: Mapped[custom_types.updated_at_T]
    users: Mapped[List["User"]] = relationship(back_populates="company")
