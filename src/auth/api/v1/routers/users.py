from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import UUID4

from src.auth.schemas.user import (
    UpdateUserSchema,
    UserSchema,
)
from src.auth.services.authorization import AuthorizationService
from src.auth.services.user import UserService
from src.auth.units_of_work.user import UserUnitOfWork
from src.schemas.responses import BaseNotFoundResponse


router = APIRouter()


@router.put(
    "/{user_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": BaseNotFoundResponse},
    },
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: UUID4,
    updated_user_data: UpdateUserSchema,
    authenticated_user: UserSchema = Depends(
        AuthorizationService.get_current_auth_user,
    ),
    uow: UserUnitOfWork = Depends(UserUnitOfWork),
):
    updated_user = await UserService.update_user(
        uow,
        user_id,
        updated_user_data.first_name,
        updated_user_data.last_name,
    )

    if not updated_user:
        return JSONResponse(
            content=BaseNotFoundResponse(
                reason="User not found."
            ).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return UserSchema.model_validate(updated_user)
