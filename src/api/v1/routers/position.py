from fastapi import APIRouter, Depends, status

from src.auth.services.authorization import AuthorizationService
from src.schemas.responses import (
    BaseNotFoundResponse,
    BaseErrorResponse,
    BaseResponse,
)
from src.structure.services.position import PositionService
from src.structure.schemas.division_position import (
    CreateDivisionPositionSchema,
    DivisionPositionSchema,
    RoleDivisionPositionSchema,
    UserDivisionPositionSchema,
)
from src.structure.schemas.position import (
    CreatePositionSchema,
    UpdatePositionSchema,
)
from src.structure.schemas.responses import (
    DivisionPositionResponse,
    PositionCreateResponse,
    PositionResponse,
)
from src.utils.unit_of_work import UnitOfWork


router = APIRouter()


@router.post(
    "/",
    response_model=PositionCreateResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AuthorizationService.get_current_auth_admin)],
)
async def create_position(
    position: CreatePositionSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await PositionService.create_position(uow, position.title)
    return result


@router.get(
    "/{position_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": BaseNotFoundResponse},
    },
    response_model=PositionResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_current_auth_user)],
)
async def get_position(
    position_id: str,
    uow: UnitOfWork = Depends(UnitOfWork),

):
    result = await PositionService.get_position(uow, position_id)
    return result


@router.put(
    "/{position_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": BaseNotFoundResponse},
    },
    response_model=PositionResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_current_auth_admin)],
)
async def update_position(
    position_id: str,
    updated_data: UpdatePositionSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await PositionService.update_position_by_id(
        uow,
        position_id,
        updated_data.model_dump(),
    )
    return result


@router.delete(
    "/{position_id}",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_current_auth_admin)],
)
async def delete_position(
    position_id: str,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await PositionService.delete_position(uow, position_id)
    return result


@router.post(
    "/assigned",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BaseErrorResponse},
    },
    response_model=CreateDivisionPositionSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AuthorizationService.get_current_auth_admin)],
)
async def assign_position_to_division(
    div_pos_data: CreateDivisionPositionSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await PositionService.assign_position_to_division(
        uow,
        div_pos_data.position_id,
        div_pos_data.division_id,
        div_pos_data.role,
    )
    return result


@router.delete(
    "/assigned/{div_pos_id}",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_current_auth_admin)],
)
async def remove_position_from_division(
    div_pos_id: str,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await PositionService.remove_position_from_division(
        uow,
        div_pos_id,
    )
    return result


@router.put(
    "/assigned/{div_pos_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": BaseNotFoundResponse},
    },
    response_model=DivisionPositionResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_current_auth_admin)],
)
async def update_division_position(
    div_pos_id: str,
    role: RoleDivisionPositionSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await PositionService.update_division_position(
        uow,
        div_pos_id,
        role.model_dump()
    )
    return result


@router.get(
    "/assigned/{div_pos_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": BaseNotFoundResponse},
    },
    response_model=DivisionPositionResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_current_auth_user)],
)
async def get_division_position(
    div_pos_id: str,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await PositionService.get_division_position(
        uow,
        div_pos_id,
    )
    return result


@router.post(
    "/assigned/{div_pos_id}/user",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": BaseNotFoundResponse},
    },
    response_model=DivisionPositionResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_current_auth_admin)],
)
async def assign_user_to_position(
    div_pos_id: str,
    user_data: UserDivisionPositionSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await PositionService.update_division_position(
        uow,
        div_pos_id,
        user_data.model_dump(),
    )
    return result


@router.delete(
    "/assigned/{div_pos_id}/user",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": BaseNotFoundResponse},
    },
    response_model=DivisionPositionResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_current_auth_admin)],
)
async def remove_user_from_position(
    div_pos_id: str,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await PositionService.update_division_position(
        uow,
        div_pos_id,
        {
            "user_id": None
        },
    )
    return result
