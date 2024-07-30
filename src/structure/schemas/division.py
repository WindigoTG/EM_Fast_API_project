from pydantic import BaseModel, Field, PlainSerializer, ConfigDict
from sqlalchemy_utils import Ltree
from typing_extensions import Annotated


class IdDivisionSchema(BaseModel):
    id: int


class BaseDivisionSchema(BaseModel):
    name: str = Field(max_length=50)


class DivisionSchema(IdDivisionSchema, BaseDivisionSchema):
    path: Annotated[
        Ltree, PlainSerializer(lambda x: x.path, return_type=str)
    ]

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class CreateDivisionSchema(BaseDivisionSchema):
    parent_path: str


class UpdateDivisionSchema(BaseModel):
    name: str | None = Field(max_length=50, default=None)
    parent_path: str | None = Field(default=None)
    parent_id: int | None = Field(default=None)
