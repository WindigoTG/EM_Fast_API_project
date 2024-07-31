from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload

from src.auth.models import Account, Secret
from src.utils.repository import SqlAlchemyRepository


class AccountRepository(SqlAlchemyRepository):
    model = Account

    async def get_by_query_one_with_related_invite_one_or_none(
        self,
        **kwargs,
    ) -> Account | None:
        query = select(self.model).filter_by(**kwargs).options(
            joinedload(Account.invite),
        )
        res: Result = await self.session.execute(query)
        return res.unique().scalar_one_or_none()

    async def get_by_query_one_with_related_secret_one_or_none(
        self,
        **kwargs,
    ) -> Account | None:
        query = select(self.model).filter_by(**kwargs).options(
            joinedload(Account.secret).subqueryload(Secret.user),
        )
        res: Result = await self.session.execute(query)
        return res.unique().scalar_one_or_none()
