from typing import Union
from uuid import uuid4

from src.auth.schemas.responses import UserAndCompanyCreatedResponse
from src.auth.utils.enums import RegistrationServiceResultEnum
from src.auth.utils.password_hasher import hash_password
from src.auth.utils.token_generator import generate_int_token
from src.utils.unit_of_work import UnitOfWork


class RegistrationService:
    @classmethod
    async def check_if_account_available(
        cls,
        uow: UnitOfWork,
        account: str,
    ) -> bool:
        async with uow:
            if (
                await uow.repositories["account"].get_by_query_one_or_none(
                    account=account,
                )
            ):
                return False
        return True

    @classmethod
    async def create_account(
        cls,
        uow: UnitOfWork,
        account: str
    ) -> RegistrationServiceResultEnum:
        async with uow:
            if (
                await uow.repositories["account"].get_by_query_one_or_none(
                    account=account,
                )
            ):
                return RegistrationServiceResultEnum.ACCOUNT_ALREADY_EXISTS

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

        # TODO: send e-mail notification

        return RegistrationServiceResultEnum.SUCCESS

    @classmethod
    async def create_account_and_user_for_company(
            cls, uow: UnitOfWork,
            account: str,
            company_id: Union[int, str, uuid4],
            first_name: str,
            last_name: str,
    ) -> RegistrationServiceResultEnum:
        async with uow:
            company = (
                await uow.repositories["company"].get_by_query_one_or_none(
                    id=company_id,
                )
            )

            if not company:
                return RegistrationServiceResultEnum.COMPANY_DOES_NOT_EXIST

            if (
                await uow.repositories["account"].get_by_query_one_or_none(
                    account=account,
                )
            ):
                return RegistrationServiceResultEnum.ACCOUNT_ALREADY_EXISTS

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
                hashed_password='',
            )

        # TODO: send e-mail notification

        return RegistrationServiceResultEnum.SUCCESS

    @classmethod
    async def verify_account(
        cls,
        uow: UnitOfWork,
        account: str,
        invite_token: int,
    ) -> RegistrationServiceResultEnum:
        async with uow:
            account_to_validate = (
                await uow.repositories[
                    "account"
                ].get_by_query_one_with_related_invite_one_or_none(
                    account=account
                )
            )
            if not account_to_validate:
                return RegistrationServiceResultEnum.ACCOUNT_DOES_NOT_EXIST

            if account_to_validate.is_verified:
                return RegistrationServiceResultEnum.ACCOUNT_ALREADY_VERIFIED

            if account_to_validate.invite.token != invite_token:
                return RegistrationServiceResultEnum.WRONG_TOKEN

            await uow.repositories["account"].update_one_by_id(
                account_to_validate.id,
                {"is_verified": True}
            )
            return RegistrationServiceResultEnum.SUCCESS

    @classmethod
    async def create_user_and_company(
        cls,
        uow: UnitOfWork,
        account: str,
        password: str,
        first_name: str,
        last_name: str,
        company_name: str,
    ) -> tuple[
        RegistrationServiceResultEnum,
        UserAndCompanyCreatedResponse | None
    ]:
        async with uow:
            account = await (
                uow.repositories[
                    "account"
                ].get_by_query_one_with_related_secret_one_or_none(
                    account=account,
                )
            )
            if not account:
                return (
                    RegistrationServiceResultEnum.ACCOUNT_DOES_NOT_EXIST,
                    None,
                )

            if not account.is_verified:
                return (
                    RegistrationServiceResultEnum.ACCOUNT_NOT_VERIFIED,
                    None,
                )

            if account.secret:
                return (
                    RegistrationServiceResultEnum.ACCOUNT_IN_USE,
                    None,
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

            return (
                RegistrationServiceResultEnum.SUCCESS,
                UserAndCompanyCreatedResponse(
                    user_id=user_id,
                    company_id=company_id,
                )
            )
