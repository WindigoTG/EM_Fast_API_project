from pydantic import BaseModel, UUID4


class SecretSchema(BaseModel):
    account_id: UUID4
    user_id: UUID4
    hashed_password: str
