from pydantic import BaseModel, EmailStr, Field, UUID4


class IdAccountSchema(BaseModel):
    id: UUID4


class CreateAccountSchema(BaseModel):
    account: EmailStr = Field(max_length=50)


class VerifyAccountSchema(BaseModel):
    account: EmailStr = Field(max_length=50)
    invite_token: int


class AccountSchema(IdAccountSchema, CreateAccountSchema):
    is_verified: bool
