from pydantic import BaseModel, Field, UUID4


class IdAccountSchema(BaseModel):
    id: UUID4


class CreateAccountSchema(BaseModel):
    account: str = Field(max_length=50)


class AccountSchema(IdAccountSchema, CreateAccountSchema):
    is_verified: bool
