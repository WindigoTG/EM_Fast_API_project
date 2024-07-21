from sqlalchemy.orm import Mapped

from src.models import BaseModel, custom_types


class Account(BaseModel):
    __tablename__ = "account"

    id: Mapped[custom_types.uuid_pk_T]
    account: Mapped[custom_types.str_50_T]
    is_verified: Mapped[bool]
