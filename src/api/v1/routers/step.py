from fastapi import APIRouter, Depends, status
from pydantic import UUID4

from src.auth.services.authorization import AuthorizationService
from src.schemas.responses import (
    BaseErrorResponse,
    BaseNotFoundResponse,
    BaseResponse,
)
from src.tasks.schemas.responses import StepCreateResponse, StepResponse
from src.tasks.schemas.step import CreateStepSchema, UpdateStepSchema
from src.tasks.services import StepService
from src.utils.unit_of_work import UnitOfWork

router = APIRouter()


@router.post(
    "/",
    response_model=StepCreateResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AuthorizationService.get_current_auth_user)]
)
async def create_step(
    step_data: CreateStepSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await StepService.create_step(uow, step_data)
    return result


@router.get(
    "/{step_id}",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BaseErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": BaseNotFoundResponse},
    },
    response_model=StepResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_current_auth_user)],
)
async def get_step(
    step_id: UUID4,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await StepService.get_step(uow, step_id)
    return result


@router.delete(
    "/{step_id}",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_current_auth_user)],
)
async def delete_step(
    step_id: UUID4,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await StepService.delete_step(uow, step_id)
    return result


@router.put(
    "/{step_id}",
    responses={status.HTTP_404_NOT_FOUND: {"model": BaseNotFoundResponse}},
    response_model=StepResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_current_auth_user)]
)
async def update_task(
    step_id: UUID4,
    step_data: UpdateStepSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await StepService.update_step(uow, step_id, step_data)
    return result
