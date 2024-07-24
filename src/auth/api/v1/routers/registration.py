from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.schemas.account import CreateAccountSchema, VerifyAccountSchema
from src.auth.schemas.responses import (
    AccountAvailableResponse,
    AccountCreateResponse,
    UserAndCompanyCreatedResponse,
)
from src.auth.schemas.user import CreateUserWithCompanySchema
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
