from typing import Union
from uuid import uuid4

from src.utils.service import BaseService
from src.auth.models.user import User
from src.auth.units_of_work.user import UserUnitOfWork


class UserService(BaseService):
    base_repository = "user"

    @classmethod
    async def update_user(
        cls,
        uow: UserUnitOfWork,
        user_id: Union[int, str, uuid4],
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> User:
        async with uow:
            updated_user = (
                await uow.repositories[cls.base_repository].update_one_by_id(
                    user_id,
                    {
                        "first_name": first_name,
                        "last_name": last_name,
                    }
                )
            )

            return updated_user
