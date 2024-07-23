from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.models import BaseModel, custom_types


class Invite(BaseModel):
    __tablename__ = "invite"

    id: Mapped[custom_types.uuid_pk_T]
    token: Mapped[int]
    account_id: Mapped[uuid4] = mapped_column(ForeignKey("account.id", ondelete="CASCADE"))
    account: Mapped["Account"] = relationship(
        back_populates="invite",
        single_parent=True,
    )
