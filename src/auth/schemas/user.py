from pydantic import BaseModel, EmailStr, Field, UUID4, ConfigDict


class IdUserSchema(BaseModel):
    id: UUID4


class BaseUserSchema(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)


class UserAccountSchema(BaseUserSchema):
    account: EmailStr


class CreateUserSchema(UserAccountSchema):
    password: str = Field(alias="pass")


class CreateUserWithCompanySchema(CreateUserSchema):
    company_name: str = Field(max_length=50)


class CreateUserWithAccountSchema(UserAccountSchema):
    ...


class UserSchema(IdUserSchema, BaseUserSchema):
    company_id: UUID4
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)


class UpdateUserSchema(BaseModel):
    first_name: str | None = Field(max_length=50, default=None)
    last_name: str | None = Field(max_length=50, default=None)
