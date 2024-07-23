from uuid import uuid4

from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel


class Secret(BaseModel):
    __tablename__ = "secret"

    account_id: Mapped[uuid4] = mapped_column(
        UUID,
        ForeignKey("account.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[uuid4] = mapped_column(
        UUID,
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    )
    hashed_password: Mapped[str]
    account: Mapped["Account"] = relationship(back_populates="secret")
    user: Mapped["User"] = relationship(back_populates="secret")
