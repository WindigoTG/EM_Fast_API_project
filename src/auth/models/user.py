from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel, custom_types


class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[custom_types.uuid_pk_T]
    first_name: Mapped[custom_types.str_50_T]
    last_name: Mapped[custom_types.str_50_T]
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[custom_types.created_at_T]
    updated_at: Mapped[custom_types.updated_at_T]
    account: Mapped["Account"] = relationship(
        secondary="secret",
        back_populates="user",
    )
    secret: Mapped["Secret"] = relationship(back_populates="user")
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    company: Mapped["Company"] = relationship(back_populates="users")
