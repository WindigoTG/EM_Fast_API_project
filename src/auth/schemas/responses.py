from pydantic import UUID4

from src.schemas.responses import BaseResponse, BaseCreateResponse
from src.auth.schemas.user import UserSchema


class AccountAvailableResponse(BaseResponse):
    result: bool


class AccountCreateResponse(BaseCreateResponse):
    ...


class UserAndCompanyCreatedResponse(BaseCreateResponse):
    user_id: UUID4
    company_id: UUID4


class UpdatedUserResponse(BaseResponse):
    payload: UserSchema
