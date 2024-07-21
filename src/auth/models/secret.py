from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel, custom_types


class Secret(BaseModel):
    __tablename__ = "secret"

    account_id: Mapped[custom_types.uuid_pk_T] = mapped_column(
        ForeignKey("account.id"),
        primary_key=True,
        onupdate="CASCADE",
    )
    user_id: Mapped[custom_types.uuid_pk_T] = mapped_column(
        ForeignKey("user.id"),
        primary_key=True,
        onupdate="CASCADE",
    )
    hashed_password = Mapped[str]
    account: Mapped["Account"] = relationship(back_populates="secret")
    user: Mapped["User"] = relationship(back_populates="secret")
