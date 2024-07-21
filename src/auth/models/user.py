from sqlalchemy.orm import Mapped, relationship

from src.models import BaseModel, custom_types


class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[custom_types.uuid_pk_T]
    first_name: Mapped[custom_types.str_50_T]
    last_name: Mapped[custom_types.str_50_T]
    account: Mapped["Account"] = relationship(
        secondary="secret",
        back_populates="user",
    )

    secret: Mapped["Secret"] = relationship(back_populates="user")
