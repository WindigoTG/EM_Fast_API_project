from pydantic import BaseModel, Field, UUID4


class IdUserSchema(BaseModel):
    id: UUID4


class BaseUserSchema(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)


class CreateUserSchema(BaseUserSchema):
    company_name: str = Field(max_length=50)
    password: str = Field(alias="pass")
    account: str


class UserSchema(IdUserSchema, BaseUserSchema):
    company_id: UUID4
    is_admin: bool
