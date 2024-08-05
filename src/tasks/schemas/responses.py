from src.schemas.responses import BaseCreateResponse, BaseResponse
from src.tasks.schemas.step import StepSchema
from src.tasks.schemas.task import TaskSchema


class TaskCreateResponse(BaseCreateResponse):
    data: TaskSchema


class TaskResponse(BaseResponse):
    data: TaskSchema


class StepCreateResponse(BaseCreateResponse):
    data: StepSchema


class StepResponse(BaseResponse):
    data: StepSchema
