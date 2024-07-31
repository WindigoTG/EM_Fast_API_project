from typing import Any

from fastapi import status
from sqlalchemy.exc import IntegrityError

from schemas.responses import (
    BaseResponse,
)
from src.auth.tasks.tasks import send_email_registration_token
from src.auth.schemas.responses import (
    AccountAvailableResponse,
    AccountCreateResponse,
    UserAndCompanyCreatedResponse,
)
from src.auth.schemas.user import UserSchema
from src.auth.utils.enums import RegistrationServiceResultEnum
from src.auth.utils.password_hasher import hash_password
from src.auth.utils.token_generator import generate_int_token
from src.utils.unit_of_work import UnitOfWork
from src.utils.response_factory import ResponseFactory


class RegistrationService:
    @classmethod
    async def check_if_account_available(
        cls,
        uow: UnitOfWork,
        account: str,
    ) -> AccountAvailableResponse:
        is_available = True
        async with uow:
            if (
                await uow.repositories["account"].get_by_query_one_or_none(
                    account=account,
                )
            ):
                is_available = False

        return AccountAvailableResponse(
            result=is_available,
        )

    @classmethod
    async def create_account(
        cls,
        uow: UnitOfWork,
        account: str
    ) -> Any:
        async with uow:
            if (
                await uow.repositories["account"].get_by_query_one_or_none(
                    account=account,
                )
            ):
                return ResponseFactory.get_base_error_response(
                    "Account already exists."
                )

            new_account_id = (
                await uow.repositories["account"].add_one_and_get_id(
                    account=account,
                )
            )
            invite_token = generate_int_token()
            await uow.repositories["invite"].add_one(
                account_id=new_account_id,
                token=invite_token,
            )

        send_email_registration_token.delay(invite_token, account)

        return AccountCreateResponse

    @classmethod
    async def verify_account(
        cls,
        uow: UnitOfWork,
        account: str,
        invite_token: int,
    ) -> Any:
        async with uow:
            account_to_validate = (
                await uow.repositories[
                    "account"
                ].get_by_query_one_with_related_invite_one_or_none(
                    account=account
                )
            )
            if not account_to_validate:
                return ResponseFactory.get_base_error_response(
                    "Account does not exist."
                )

            if account_to_validate.is_verified:
                return ResponseFactory.get_base_error_response(
                    "Account already verified."
                )

            if account_to_validate.invite.token != invite_token:
                return ResponseFactory.get_base_error_response(
                    "Incorrect token."
                )

            await uow.repositories["account"].update_one_by_id(
                account_to_validate.id,
                {"is_verified": True}
            )
            return BaseResponse()

    @classmethod
    async def create_user_and_company(
        cls,
        uow: UnitOfWork,
        account: str,
        password: str,
        first_name: str,
        last_name: str,
        company_name: str,
    ) -> Any:
        async with uow:
            account = await (
                uow.repositories[
                    "account"
                ].get_by_query_one_with_related_secret_one_or_none(
                    account=account,
                )
            )
            if not account:
                return ResponseFactory.get_base_error_response(
                    "Account does not exist."
                )

            if not account.is_verified:
                return ResponseFactory.get_base_error_response(
                    "Account not verified."
                )

            if account.secret:
                return ResponseFactory.get_base_error_response(
                    "User already exists."
                )

            company_id = await uow.repositories["company"].add_one_and_get_id(
                name=company_name,
            )

            user_id = await uow.repositories["user"].add_one_and_get_id(
                first_name=first_name,
                last_name=last_name,
                company_id=company_id,
                is_admin=True,
            )

            hashed_password = hash_password(password)

            await uow.repositories["secret"].add_one(
                account_id=account.id,
                user_id=user_id,
                hashed_password=hashed_password,
            )

            return UserAndCompanyCreatedResponse(
                user_id=user_id,
                company_id=company_id,
            )

    @classmethod
    async def create_account_and_user_for_company(
            cls, uow: UnitOfWork,
            company_admin: UserSchema,
            account: str,
            first_name: str,
            last_name: str,
    ) -> Any:

        company_id = company_admin.company_id

        async with uow:
            company = (
                await uow.repositories["company"].get_by_query_one_or_none(
                    id=company_id,
                )
            )

            if not company:
                return ResponseFactory.get_not_found_response(
                    "Company does not exist."
                )

            if (
                await uow.repositories["account"].get_by_query_one_or_none(
                    account=account,
                )
            ):
                return ResponseFactory.get_base_error_response(
                    "Account already exists."
                )

            new_account = await uow.repositories[
                "account"].add_one_and_get_obj(
                account=account,
            )
            invite_token = generate_int_token()
            await uow.repositories["invite"].add_one(
                account_id=new_account.id,
                token=invite_token,
            )

            user = await uow.repositories["user"].add_one_and_get_obj(
                first_name=first_name,
                last_name=last_name,
                company_id=company.id,
                is_admin=False,
            )

            await uow.repositories["secret"].add_one(
                account_id=new_account.id,
                user_id=user.id,
                hashed_password=b'',
            )

        send_email_registration_token.delay(invite_token, account)

        return AccountCreateResponse

    @classmethod
    async def change_account(
        cls, uow: UnitOfWork,
        user: UserSchema,
        account: str,
        new_account: str
    ) -> Any:
        async with uow:
            account = await (
                uow.repositories[
                    "account"
                ].get_by_query_one_with_related_secret_one_or_none(
                    account=account,
                )
            )
            if not account:
                return ResponseFactory.get_not_found_response(
                    "Account does not exist."
                )

            if not account.is_verified or not account.secret:
                return ResponseFactory.get_base_error_response(
                    "Unable to change email."
                )

            if not account.secret.user_id == user.id:
                return ResponseFactory.get_base_error_response(
                    "Unable to change email.",
                    status_code=status.HTTP_403_FORBIDDEN,
                )

            if account == new_account:
                return RegistrationServiceResultEnum.SUCCESS

            try:
                await (
                    uow.repositories[
                        "account"
                    ].update_one_by_id(account.id, {"account": new_account})
                )
            except IntegrityError:
                return ResponseFactory.get_base_error_response(
                    "Email occupied."
                )

            return BaseResponse()
