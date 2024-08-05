from pydantic import BaseModel, Field, UUID4, ConfigDict


class IdStepSchema(BaseModel):
    id: UUID4


class CreateStepSchema(BaseModel):
    title: str = Field(max_length=50)
    task_id: UUID4


class StepSchema(IdStepSchema, CreateStepSchema):
    is_complete: bool

    model_config = ConfigDict(from_attributes=True)


class UpdateStepSchema(BaseModel):
    title: str | None = Field(max_length=50, default=None)
    is_complete: bool | None = Field(default=None)
