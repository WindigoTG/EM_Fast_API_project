from pydantic import BaseModel, UUID4


class IdInviteSchema(BaseModel):
    id: UUID4


class CreateInviteSchema(BaseModel):
    token: int
    account_id: UUID4


class InviteSchema(IdInviteSchema, CreateInviteSchema):
    ...
