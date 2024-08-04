from fastapi import APIRouter, Depends, status

from src.auth.services.authorization import AuthorizationService
from src.models import User
from src.schemas.responses import (
    BaseErrorResponse,
    BaseNotFoundResponse,
    BaseResponse,
)
from src.tasks.schemas.responses import TaskCreateResponse, TaskResponse
from src.tasks.schemas.task import CreateTaskSchema, UpdateTaskSchema
from src.tasks.services import TaskService
from src.utils.unit_of_work import UnitOfWork

router = APIRouter()


@router.post(
    "/",
    response_model=TaskCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_data: CreateTaskSchema,
    author: User = Depends(AuthorizationService.get_current_auth_user),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await TaskService.create_task(uow, author, task_data)
    return result


@router.get(
    "/{task_id}",
    responses={status.HTTP_404_NOT_FOUND: {"model": BaseNotFoundResponse}},
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_current_auth_user)],
)
async def get_task(
    task_id: str,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await TaskService.get_task(uow, task_id)
    return result


@router.delete(
    "/{task_id}",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BaseErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": BaseNotFoundResponse},
    },
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_task(
    task_id: str,
    user: User = Depends(AuthorizationService.get_current_auth_user),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await TaskService.delete_task(uow, task_id, user)
    return result


@router.put(
    "/{task_id}",
    responses={status.HTTP_404_NOT_FOUND: {"model": BaseNotFoundResponse}},
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_current_auth_user)]
)
async def update_task(
    task_id: str,
    task_data: UpdateTaskSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await TaskService.update_task(uow, task_id, task_data)
    return result
