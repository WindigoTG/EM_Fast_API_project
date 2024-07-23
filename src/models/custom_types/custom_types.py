from datetime import datetime
from typing import Annotated
from uuid import uuid4

from sqlalchemy import DateTime, Integer, String, text, UUID
from sqlalchemy.orm import mapped_column


sql_utc_now = text("TIMEZONE('utc', now())")

# Primary key
int_pk_T = Annotated[int, mapped_column(Integer, primary_key=True)]
uuid_pk_T = Annotated[
    uuid4,
    mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
]

# String
str_50_T = Annotated[str, mapped_column(String(50))]
str_50_unique_T = Annotated[str, mapped_column(String(50), unique=True)]
str_50_or_none_T = Annotated[
    str | None,
    mapped_column(String(50), nullable=True, default=None)
]

# DateTime
created_at_T = Annotated[datetime, mapped_column(
    DateTime,
    server_default=sql_utc_now),
]
updated_at_T = Annotated[datetime, mapped_column(
    DateTime,
    server_default=sql_utc_now,
    onupdate=sql_utc_now
)]
