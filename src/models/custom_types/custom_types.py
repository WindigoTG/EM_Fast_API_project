from uuid import uuid4
from typing import Annotated

from sqlalchemy import UUID, Integer, String
from sqlalchemy.orm import mapped_column

# Primary key
int_pk_T = Annotated[int, mapped_column(Integer, primary_key=True)]
uuid_pk_T = Annotated[
    uuid4,
    mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
]

# String
str_50_T = Annotated[str, mapped_column(String(50))]
str_50_or_none_T = Annotated[
    str | None,
    mapped_column(String(50), nullable=True, default=None)
]
