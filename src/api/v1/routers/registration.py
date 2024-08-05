from fastapi import APIRouter, Depends, status

from src.auth.schemas.account import (
    CreateAccountSchema,
    VerifyAccountSchema,
    UpdateAccountSchema,
)
from src.auth.schemas.responses import (
    AccountAvailableResponse,
    AccountCreateResponse,
    UserAndCompanyCreatedResponse,
)
from src.auth.schemas.user import (
    CreateUserWithAccountSchema,
    CreateUserWithCompanySchema,
    UserSchema,
)
from src.auth.services.authorization import AuthorizationService
from src.auth.services.registration import RegistrationService
from src.schemas.responses import BaseErrorResponse, BaseResponse
from src.utils.unit_of_work import UnitOfWork

router = APIRouter()


@router.get(
    "/check_account/{account}",
    response_model=AccountAvailableResponse,
)
async def check_account(
    account: str,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    is_available = await RegistrationService.check_if_account_available(
        uow,
        account,
    )

    return is_available


@router.post(
    "/sign-in",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BaseErrorResponse},
    },
    response_model=AccountCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_new_account(
    account: CreateAccountSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await RegistrationService.create_account(uow, account.account)
    return result


@router.post(
    "/sign-up",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BaseErrorResponse},
    },
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
)
async def verify_account(
    account: VerifyAccountSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await RegistrationService.verify_account(
        uow,
        account.account,
        account.invite_token,
    )

    return result


@router.post(
    "/sign-up-complete",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BaseErrorResponse},
    },
    response_model=UserAndCompanyCreatedResponse,
    status_code=status.HTTP_201_CREATED,
)
async def verify_account(
    user: CreateUserWithCompanySchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = await RegistrationService.create_user_and_company(
        uow,
        user.account,
        user.password,
        user.first_name,
        user.last_name,
        user.company_name,
    )
    return result


@router.post(
    "/register-employee",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BaseErrorResponse},
        status.HTTP_403_FORBIDDEN: {"model": BaseErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": BaseErrorResponse},
    },
    response_model=AccountCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_employee(
    new_user_data: CreateUserWithAccountSchema,
    company_admin: UserSchema = Depends(
        AuthorizationService.get_current_auth_admin,
    ),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = (
        await RegistrationService.create_account_and_user_for_company(
            uow,
            company_admin,
            new_user_data.account,
            new_user_data.first_name,
            new_user_data.last_name,
        )
    )
    return result


@router.put(
    "/update-email",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BaseErrorResponse},
        status.HTTP_403_FORBIDDEN: {"model": BaseErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": BaseErrorResponse},
    },
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
)
async def update_email(
    new_account_data: UpdateAccountSchema,
    user: UserSchema = Depends(
        AuthorizationService.get_current_auth_user,
    ),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    result = (
        await RegistrationService.change_account(
            uow,
            user,
            new_account_data.account,
            new_account_data.new_account,
        )
    )
    return result
