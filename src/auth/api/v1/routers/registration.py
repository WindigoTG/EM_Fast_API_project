from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

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
from src.auth.units_of_work.auth import AuthUnitOfWork
from src.auth.utils.enums import RegistrationServiceResultEnum
from src.schemas.responses import BaseErrorResponse, BaseResponse

router = APIRouter()


@router.get(
    "/check_account/{account}",
    response_model=AccountAvailableResponse,
)
async def check_account(
    account: str,
    uow: AuthUnitOfWork = Depends(AuthUnitOfWork),
):
    is_available = await RegistrationService.check_if_account_available(
        uow,
        account,
    )
    return AccountAvailableResponse(
        result=is_available,
    )


@router.post(
    "/register",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BaseErrorResponse},
    },
    response_model=AccountCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_new_account(
    account: CreateAccountSchema,
    uow: AuthUnitOfWork = Depends(AuthUnitOfWork),
):
    result = await RegistrationService.create_account(uow, account.account)
    match result:
        case RegistrationServiceResultEnum.ACCOUNT_ALREADY_EXISTS:
            return JSONResponse(
                content=BaseErrorResponse(
                    reason="Account already exists."
                ).model_dump(),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        case RegistrationServiceResultEnum.SUCCESS:
            return AccountCreateResponse


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
    uow: AuthUnitOfWork = Depends(AuthUnitOfWork),
):
    result = await RegistrationService.verify_account(
        uow,
        account.account,
        account.invite_token,
    )
    match result:
        case RegistrationServiceResultEnum.ACCOUNT_ALREADY_VERIFIED:
            return JSONResponse(
                content=BaseErrorResponse(
                    reason="Account already verified."
                ).model_dump(),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        case RegistrationServiceResultEnum.ACCOUNT_DOES_NOT_EXIST:
            return JSONResponse(
                content=BaseErrorResponse(
                    reason="Account does not exist."
                ).model_dump(),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        case RegistrationServiceResultEnum.WRONG_TOKEN:
            return JSONResponse(
                content=BaseErrorResponse(
                    reason="Incorrect token."
                ).model_dump(),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        case RegistrationServiceResultEnum.SUCCESS:
            return BaseResponse


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
    uow: AuthUnitOfWork = Depends(AuthUnitOfWork),
):
    result, response = await RegistrationService.create_user_and_company(
        uow,
        user.account,
        user.password,
        user.first_name,
        user.last_name,
        user.company_name,
    )
    match result:
        case RegistrationServiceResultEnum.ACCOUNT_NOT_VERIFIED:
            return JSONResponse(
                content=BaseErrorResponse(
                    reason="Account not verified."
                ).model_dump(),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        case RegistrationServiceResultEnum.ACCOUNT_DOES_NOT_EXIST:
            return JSONResponse(
                content=BaseErrorResponse(
                    reason="Account does not exist."
                ).model_dump(),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        case RegistrationServiceResultEnum.ACCOUNT_IN_USE:
            return JSONResponse(
                content=BaseErrorResponse(
                    reason="User already exists."
                ).model_dump(),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        case RegistrationServiceResultEnum.SUCCESS:
            return response


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
    uow: AuthUnitOfWork = Depends(AuthUnitOfWork),
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

    match result:
        case RegistrationServiceResultEnum.ACCOUNT_ALREADY_EXISTS:
            return JSONResponse(
                content=BaseErrorResponse(
                    reason="Account already exists."
                ).model_dump(),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        case RegistrationServiceResultEnum.COMPANY_DOES_NOT_EXIST:
            return JSONResponse(
                content=BaseErrorResponse(
                    status=404,
                    reason="Company does not exist."
                ).model_dump(),
                status_code=status.HTTP_404_NOT_FOUND,
            )
        case RegistrationServiceResultEnum.SUCCESS:
            return AccountCreateResponse


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
    uow: AuthUnitOfWork = Depends(AuthUnitOfWork),
):
    result = (
        await RegistrationService.change_account(
            uow,
            user,
            new_account_data.account,
            new_account_data.new_account,
        )
    )

    match result:
        case (
            RegistrationServiceResultEnum.ACCOUNT_NOT_VERIFIED |
            RegistrationServiceResultEnum.USER_NOT_CREATED
        ):
            return JSONResponse(
                content=BaseErrorResponse(
                    reason="Unable to change email."
                ).model_dump(),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        case RegistrationServiceResultEnum.ACCOUNT_DOES_NOT_EXIST:
            return JSONResponse(
                content=BaseErrorResponse(
                    status=404,
                    reason="Account does not exist."
                ).model_dump(),
                status_code=status.HTTP_404_NOT_FOUND,
            )
        case RegistrationServiceResultEnum.NOT_ALLOWED:
            return JSONResponse(
                content=BaseErrorResponse(
                    status=403,
                    reason="Unable to change email."
                ).model_dump(),
                status_code=status.HTTP_403_FORBIDDEN,
            )
        case RegistrationServiceResultEnum.ACCOUNT_ALREADY_EXISTS:
            return JSONResponse(
                content=BaseErrorResponse(
                    reason="Email occupied."
                ).model_dump(),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        case RegistrationServiceResultEnum.SUCCESS:
            return BaseResponse
