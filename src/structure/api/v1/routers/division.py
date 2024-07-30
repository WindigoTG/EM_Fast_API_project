from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.schemas.user import UserSchema
from src.auth.services.authorization import AuthorizationService
from src.schemas.responses import BaseNotFoundResponse, BaseErrorResponse
from src.structure.services.division import DivisionService
from src.structure.units_of_work.division import DivisionUnitOfWork
from src.structure.schemas.division import DivisionSchema, UpdateDivisionSchema
from src.structure.schemas.responses import (
    DivisionCreateResponse,
    DivisionResponse,
)
from src.structure.utils.enums import DivisionServiceOperationResult


router = APIRouter()


@router.post(
    "/",
    response_model=DivisionCreateResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AuthorizationService.get_current_auth_admin)]
)
async def create_division(
    name: str,
    uow: DivisionUnitOfWork = Depends(DivisionUnitOfWork),
):
    new_division = await DivisionService.add_one_and_get_obj(uow, name=name)

    return DivisionCreateResponse(
        data=DivisionSchema.model_validate(new_division)
    )


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
    uow: DivisionUnitOfWork = Depends(DivisionUnitOfWork),
):
    division = await DivisionService.get_by_query_one_or_none(
        uow,
        id=division_id,
    )

    if division:
        return DivisionResponse(data=DivisionSchema.model_validate(division))

    return JSONResponse(
        content=BaseNotFoundResponse(
            reason=f"Division {division_id} does not exist."
        ).model_dump(),
        status_code=status.HTTP_404_NOT_FOUND,
    )


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
    uow: DivisionUnitOfWork = Depends(DivisionUnitOfWork),
):
    result, updated_division = await DivisionService.update_one_by_id(
        uow,
        division_id,
        updated_data.model_dump(),
    )
    match result:
        case DivisionServiceOperationResult.DIVISION_NOT_FOUND:
            return JSONResponse(
                content=BaseNotFoundResponse(
                    reason=f"Division {division_id} does not exist."
                ).model_dump(),
                status_code=status.HTTP_404_NOT_FOUND,
            )
        case DivisionServiceOperationResult.INCORRECT_PARENT:
            return JSONResponse(
                content=BaseErrorResponse(
                    reason=f"Incorrect parent"
                ).model_dump(),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    return DivisionResponse(
        data=DivisionSchema.model_validate(updated_division),
    )
