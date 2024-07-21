from sqlalchemy.orm import Mapped

from src.models import BaseModel, custom_types


class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[custom_types.uuid_pk_T]
    first_name: Mapped[custom_types.str_50_T]
    last_name: Mapped[custom_types.str_50_T]
