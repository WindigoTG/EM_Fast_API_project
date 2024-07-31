from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel, custom_types


class Account(BaseModel):
    __tablename__ = "account"

    id: Mapped[custom_types.uuid_pk_T]
    account: Mapped[str] = mapped_column(String(50), unique=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    user: Mapped["User"] = relationship(
        secondary="secret",
        back_populates="account",
    )
    secret: Mapped["Secret"] = relationship(back_populates="account")
    invite: Mapped["Invite"] = relationship(back_populates="account")
