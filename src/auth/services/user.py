from typing import Union, Any
from uuid import uuid4

from fastapi import status
from src.auth.schemas.user import UserSchema
from src.utils.service import BaseService
from src.models.user import User
from src.utils.response_factory import ResponseFactory
from src.utils.unit_of_work import UnitOfWork


class UserService(BaseService):
    base_repository = "user"

    @classmethod
    async def update_user(
        cls,
        uow: UnitOfWork,
        user_id: Union[int, str, uuid4],
        request_user: User,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> Any:

        if not request_user.id == user_id:
            return ResponseFactory.get_base_error_response(
                "Forbidden",
                status_code=status.HTTP_403_FORBIDDEN
            )

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

            if not updated_user:
                ResponseFactory.get_not_found_response(
                    "User not found."
                )

            return UserSchema.model_validate(updated_user)
