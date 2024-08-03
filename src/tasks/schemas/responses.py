from src.schemas.responses import BaseCreateResponse, BaseResponse
from src.tasks.schemas.task import TaskSchema


class TaskCreateResponse(BaseCreateResponse):
    data: TaskSchema


class TaskResponse(BaseResponse):
    data: TaskSchema
