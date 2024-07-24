import pytest

from src.auth.services.registration import RegistrationService
from src.auth.units_of_work.auth import AuthUnitOfWork
from tests.fakes.auth.fake_params import (
    TEST_CHECK_IF_ACCOUNT_AVAILABLE_PARAMS,
    TEST_CREATE_ACCOUNT_PARAMS,
    TEST_VERIFY_ACCOUNT_PARAMS,
    TEST_CREATE_USER_AND_COMPANY_PARAMS,
    TEST_CREATE_ACCOUNT_AND_USER_FOR_COMPANY_PARAMS,
)


class TestRegistrationService:
    class _RegistrationService(RegistrationService):
        ...

    @pytest.mark.parametrize(
        "kwargs, expected_result, expectation",
        TEST_CHECK_IF_ACCOUNT_AVAILABLE_PARAMS,
    )
    async def test_check_if_account_available(
        self,
        kwargs,
        expected_result,
        expectation,
        add_accounts,
        clear_accounts,
        get_accounts,
    ):
        await clear_accounts()
        await add_accounts()

        with expectation:
            is_available = await (
                self._RegistrationService.check_if_account_available(
                    uow=AuthUnitOfWork(),
                    **kwargs,
                )
            )

            assert is_available is expected_result

    @pytest.mark.parametrize(
        "kwargs, expected_result, expectation",
        TEST_CREATE_ACCOUNT_PARAMS,
    )
    async def test_create_account(
        self,
        kwargs,
        expected_result,
        expectation,
        clear_accounts,
        clear_invites,
        add_accounts
    ):
        await clear_invites()
        await clear_accounts()
        await add_accounts()

        with expectation:
            result = await self._RegistrationService.create_account(
                uow=AuthUnitOfWork(),
                **kwargs,
            )
            assert result == expected_result

    @pytest.mark.parametrize(
        "kwargs, expected_result, expectation",
        TEST_VERIFY_ACCOUNT_PARAMS,
    )
    async def test_verify_account(
            self,
            kwargs,
            expected_result,
            expectation,
            add_accounts,
            add_invites,
            clear_accounts,
            clear_invites,
    ):
        await clear_invites()
        await clear_accounts()

        await add_accounts()
        await add_invites()

        with expectation:
            result = await self._RegistrationService.verify_account(
                uow=AuthUnitOfWork(),
                **kwargs,
            )
            assert result == expected_result

    @pytest.mark.parametrize(
        "kwargs, expected_result, expectation",
        TEST_CREATE_USER_AND_COMPANY_PARAMS,
    )
    async def test_create_user_and_company(
        self,
        kwargs,
        expected_result,
        expectation,
        add_all_entities,
        clear_all_entities,
    ):
        await clear_all_entities()
        await add_all_entities()

        with expectation:
            result, _ = (
                await self._RegistrationService.create_user_and_company(
                    uow=AuthUnitOfWork(),
                    **kwargs,
                )
            )
            assert result == expected_result

    @pytest.mark.parametrize(
        "kwargs, expected_result, expectation",
        TEST_CREATE_ACCOUNT_AND_USER_FOR_COMPANY_PARAMS,
    )
    async def test_create_account_and_user_for_company(
            self,
            kwargs,
            expected_result,
            expectation,
            add_all_entities,
            clear_all_entities,
    ):
        await clear_all_entities()
        await add_all_entities()

        with expectation:
            result = (
                await self._RegistrationService.create_account_and_user_for_company(
                    uow=AuthUnitOfWork(),
                    **kwargs,
                )
            )
            assert result == expected_result

