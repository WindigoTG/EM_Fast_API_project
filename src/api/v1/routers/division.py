from fastapi import APIRouter, Depends, status

from src.auth.services.authorization import AuthorizationService
from src.schemas.responses import (
    BaseNotFoundResponse,
    BaseErrorResponse,
    BaseResponse,
)
from src.structure.services.division import DivisionService
from src.structure.schemas.division import UpdateDivisionSchema
from src.structure.schemas.responses import (
    DivisionCreateResponse,
    DivisionResponse,
)
from src.utils.unit_of_work import UnitOfWork


router = APIRouter()


@router.post(
    "/",
    response_model=DivisionCreateResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AuthorizationService.get_current_auth_admin)]
)
async def create_division(
    name: str,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await DivisionService.add_one_and_get_obj(uow, name=name)
    return result


@router.get(
    "/{division_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": BaseNotFoundResponse},
    },
    response_model=DivisionResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_current_auth_user)]
)
async def get_division(
    division_id: int,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await DivisionService.get_by_query_one_or_none(
        uow,
        id=division_id,
    )

    return result


@router.put(
    "/{division_id}",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BaseErrorResponse},
        status.HTTP_403_FORBIDDEN: {"model": BaseErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": BaseErrorResponse},
    },
    response_model=DivisionResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_current_auth_admin)]
)
async def update_division(
    division_id: int,
    updated_data: UpdateDivisionSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await DivisionService.update_one_by_id(
        uow,
        division_id,
        updated_data.model_dump(),
    )
    return result


@router.delete(
    "/{division_id}",
    responses={
        status.HTTP_403_FORBIDDEN: {"model": BaseErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": BaseErrorResponse},
    },
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthorizationService.get_current_auth_admin)]
)
async def delete_division(
    division_id: int,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await DivisionService.delete_by_id(uow, division_id)
    return result
