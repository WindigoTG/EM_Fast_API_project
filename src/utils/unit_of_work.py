from abc import ABC, abstractmethod
from typing import Dict

from src.database.db import async_session_maker
from src.utils.repository import SqlAlchemyRepository
from src.repositories import (
    AccountRepository,
    CompanyRepository,
    DivisionRepository,
    DivisionPositionRepository,
    InviteRepository,
    PositionRepository,
    SecretRepository,
    UserRepository,
)


class AbstractUnitOfWork(ABC):
    repositories: Dict[str, SqlAlchemyRepository]

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    """The class responsible for the atomicity of transactions"""

    def __init__(self):
        self.session_factory = async_session_maker
        self.repositories["account"] = AccountRepository(self.session)
        self.repositories["company"] = CompanyRepository(self.session)
        self.repositories["division"] = DivisionRepository(self.session)
        self.repositories["division_position"] = DivisionPositionRepository(
            self.session,
        )
        self.repositories["invite"] = InviteRepository(self.session)
        self.repositories["position"] = PositionRepository(self.session)
        self.repositories["secret"] = SecretRepository(self.session)
        self.repositories["user"] = UserRepository(self.session)

    async def __aenter__(self):
        self.session = self.session_factory()

    async def __aexit__(self, exc_type, *args):
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
