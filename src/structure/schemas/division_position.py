from pydantic import BaseModel, Field, UUID4

from src.structure.utils.enums import RoleEnum


class IdDivisionPositionSchema(BaseModel):
    id: UUID4


class RoleDivisionPositionSchema(BaseModel):
    role: RoleEnum


class UserDivisionPositionSchema(BaseModel):
    user_id: UUID4 | None = Field(default=None)


class BaseDivisionPositionSchema(
    RoleDivisionPositionSchema,
    UserDivisionPositionSchema,
):
    ...


class CreateDivisionPositionSchema(BaseDivisionPositionSchema):
    division_id: int
    position_id: UUID4


class DivisionPositionSchema(
    IdDivisionPositionSchema,
    CreateDivisionPositionSchema,
):
    ...


class UpdateDivisionPositionSchema(BaseDivisionPositionSchema):
    ...
