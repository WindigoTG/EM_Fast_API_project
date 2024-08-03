from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, UUID4

from src.auth.schemas.user import UserSchema
from src.tasks.utils.enums import TaskStatusEnum
from src.tasks.schemas.step import StepSchema


class IdTaskSchema(BaseModel):
    id: UUID4


class BaseTaskSchema(BaseModel):
    title: str = Field(max_length=50)


class CreateTaskSchema(BaseTaskSchema):
    description: str | None = Field(default=None)
    deadline: datetime | None = Field(default=None)
    approver_id: UUID4 | None = Field(default=None)
    performers: List[UUID4] | None = Field(default=None)
    observers: List[UUID4] | None = Field(default=None)


class TaskSchema(IdTaskSchema, BaseTaskSchema):
    description: str = Field(default='')
    deadline: datetime
    is_complete: bool
    author: UserSchema
    approver: UserSchema | None = Field(default=None)
    performers: List[UserSchema] = Field(default=[])
    observers: List[UserSchema] = Field(default=[])
    steps: List[StepSchema] = Field(default=[])


class UpdateStepSchema(CreateTaskSchema):
    title: str | None = Field(max_length=50, default=None)
    status: TaskStatusEnum | None = Field(default=None)
    is_completed: bool | None = Field(default=None)
