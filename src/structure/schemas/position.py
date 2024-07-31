from pydantic import BaseModel, Field, UUID4


class IdPositionSchema(BaseModel):
    id: UUID4


class CreatePositionSchema(BaseModel):
    title: str = Field(max_length=50)


class PositionSchema(IdPositionSchema, CreatePositionSchema):
    ...


class UpdatePositionSchema(CreatePositionSchema):
    ...
