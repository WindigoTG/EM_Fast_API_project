from typing import Optional

from pydantic import BaseModel, Field, UUID4


class IdCompanySchema(BaseModel):
    id: UUID4


class CreateCompanySchema(BaseModel):
    name: str = Field(max_length=50)
    description: Optional[str]


class CompanySchema(IdCompanySchema, CreateCompanySchema):
    ...
