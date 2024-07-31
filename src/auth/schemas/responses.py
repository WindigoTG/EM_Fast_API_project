from pydantic import UUID4

from src.schemas.responses import BaseResponse
from src.auth.schemas.user import UserSchema


class AccountAvailableResponse(BaseResponse):
    result: bool


class AccountCreateResponse(BaseResponse):
    status: int = 201


class UserAndCompanyCreatedResponse(BaseResponse):
    status: int = 201
    user_id: UUID4
    company_id: UUID4


class UpdatedUserResponse(BaseResponse):
    payload: UserSchema
