from copy import deepcopy
from typing import Callable, List, Sequence

import pytest
from sqlalchemy import text, Result, select, insert

from src.auth.models import Account, Company, Invite, Secret, User
from src.auth.schemas.account import AccountSchema
from src.auth.schemas.company import CompanySchema
from src.auth.schemas.invite import InviteSchema
from src.auth.schemas.secret import SecretSchema
from src.auth.schemas.user import UserSchema
from tests.fakes.auth.fake_accounts import FAKE_ACCOUNTS
from tests.fakes.auth.fake_companies import FAKE_COMPANIES
from tests.fakes.auth.fake_invites import FAKE_INVITES
from tests.fakes.auth.fake_secrets import FAKE_SECRETS
from tests.fakes.auth.fake_users import FAKE_USERS


@pytest.fixture(scope="function")
def accounts() -> List[AccountSchema]:
    return deepcopy(FAKE_ACCOUNTS)


@pytest.fixture(scope="function")
def companies() -> List[CompanySchema]:
    return deepcopy(FAKE_COMPANIES)


@pytest.fixture(scope="function")
def invites() -> List[InviteSchema]:
    return deepcopy(FAKE_INVITES)


@pytest.fixture(scope="function")
def secrets() -> List[SecretSchema]:
    return deepcopy(FAKE_SECRETS)


@pytest.fixture(scope="function")
def users() -> List[UserSchema]:
    return deepcopy(FAKE_USERS)


@pytest.fixture(scope="session")
def clear_accounts(async_session_maker) -> Callable:
    sql = text("TRUNCATE public.account RESTART IDENTITY CASCADE;")

    async def _clear_accounts():
        async with async_session_maker() as session:
            await session.execute(sql)
            await session.commit()

    return _clear_accounts


@pytest.fixture(scope="session")
def get_accounts(async_session_maker) -> Callable:
    async def _accounts() -> Sequence[Account]:
        async with async_session_maker() as session:
            res: Result = await session.execute(select(Account))
            return res.scalars().all()

    return _accounts


@pytest.fixture(scope="function")
def add_accounts(async_session_maker, accounts) -> Callable:
    async def _add_accounts() -> None:
        async with async_session_maker() as session:
            for account_schema in accounts:
                await session.execute(
                    insert(Account).values(
                        **account_schema.model_dump(),
                    )
                )
            await session.commit()

    return _add_accounts


@pytest.fixture(scope="session")
def get_invites(async_session_maker) -> Callable:
    async def _invites() -> Sequence[Invite]:
        async with async_session_maker() as session:
            res: Result = await session.execute(select(Invite))
            return res.scalars().all()

    return _invites


@pytest.fixture(scope="session")
def clear_invites(async_session_maker) -> Callable:
    sql = text("TRUNCATE public.invite RESTART IDENTITY CASCADE;")

    async def _clear_invites():
        async with async_session_maker() as session:
            await session.execute(sql)
            await session.commit()

    return _clear_invites


@pytest.fixture(scope="function")
def add_invites(async_session_maker, invites) -> Callable:
    async def _add_invites() -> None:
        async with async_session_maker() as session:
            for invite_schema in invites:
                await session.execute(
                    insert(Invite).values(
                        **invite_schema.model_dump(),
                    )
                )
            await session.commit()

    return _add_invites


@pytest.fixture(scope="session")
def clear_companies(async_session_maker) -> Callable:
    sql = text("TRUNCATE public.company RESTART IDENTITY CASCADE;")

    async def _clear_companies():
        async with async_session_maker() as session:
            await session.execute(sql)
            await session.commit()

    return _clear_companies


@pytest.fixture(scope="session")
def get_companies(async_session_maker) -> Callable:
    async def _companies() -> Sequence[Company]:
        async with async_session_maker() as session:
            res: Result = await session.execute(select(Company))
            return res.scalars().all()

    return _companies


@pytest.fixture(scope="function")
def add_companies(async_session_maker, companies) -> Callable:
    async def _add_companies() -> None:
        async with async_session_maker() as session:
            for company_schema in companies:
                await session.execute(
                    insert(Company).values(
                        **company_schema.model_dump(),
                    )
                )
            await session.commit()

    return _add_companies


@pytest.fixture(scope="session")
def clear_users(async_session_maker) -> Callable:
    sql = text("TRUNCATE public.user RESTART IDENTITY CASCADE;")

    async def _clear_users():
        async with async_session_maker() as session:
            await session.execute(sql)
            await session.commit()

    return _clear_users


@pytest.fixture(scope="session")
def get_users(async_session_maker) -> Callable:
    async def _users() -> Sequence[User]:
        async with async_session_maker() as session:
            res: Result = await session.execute(select(User))
            return res.scalars().all()

    return _users


@pytest.fixture(scope="function")
def add_users(async_session_maker, users) -> Callable:
    async def _add_users() -> None:
        async with async_session_maker() as session:
            for user_schema in users:
                await session.execute(
                    insert(User).values(
                        **user_schema.model_dump(),
                    )
                )
            await session.commit()

    return _add_users


@pytest.fixture(scope="session")
def clear_secrets(async_session_maker) -> Callable:
    sql = text("TRUNCATE public.secret RESTART IDENTITY CASCADE;")

    async def _clear_secrets():
        async with async_session_maker() as session:
            await session.execute(sql)
            await session.commit()

    return _clear_secrets


@pytest.fixture(scope="session")
def get_secrets(async_session_maker) -> Callable:
    async def _secrets() -> Sequence[Secret]:
        async with async_session_maker() as session:
            res: Result = await session.execute(select(Secret))
            return res.scalars().all()

    return _secrets


@pytest.fixture(scope="function")
def add_secrets(async_session_maker, secrets) -> Callable:
    async def _add_secrets() -> None:
        async with async_session_maker() as session:
            for secret_schema in secrets:
                await session.execute(
                    insert(Secret).values(
                        **secret_schema.model_dump()
                    )
                )

            await session.commit()

    return _add_secrets


@pytest.fixture(scope="function")
def clear_all_entities(
    clear_accounts,
    clear_companies,
    clear_invites,
    clear_secrets,
    clear_users,
) -> Callable:

    async def _clear_all_entities():
        await clear_invites()
        await clear_secrets()
        await clear_users()
        await clear_companies()
        await clear_accounts()

    return _clear_all_entities


@pytest.fixture(scope="function")
def add_all_entities(
    add_accounts,
    add_companies,
    add_invites,
    add_secrets,
    add_users,
) -> Callable:

    async def _add_all_entities():
        await add_accounts()
        await add_invites()
        await add_companies()
        await add_users()
        await add_secrets()

    return _add_all_entities
