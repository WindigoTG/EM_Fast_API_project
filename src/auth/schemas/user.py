from pydantic import BaseModel, EmailStr, Field, UUID4, ConfigDict


class IdUserSchema(BaseModel):
    id: UUID4


class BaseUserSchema(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)


class CreateUserSchema(BaseUserSchema):
    password: str = Field(alias="pass")
    account: EmailStr


class CreateUserWithCompanySchema(CreateUserSchema):
    company_name: str = Field(max_length=50)


class UserSchema(IdUserSchema, BaseUserSchema):
    company_id: UUID4
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)
