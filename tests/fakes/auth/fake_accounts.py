from uuid import uuid4

from src.auth.schemas.account import AccountSchema


FAKE_ACCOUNTS: list[AccountSchema] = [
    AccountSchema(
        id=uuid4(),
        account="unverified_test@test.com",
        is_verified=False,
    ),
    AccountSchema(
        id=uuid4(),
        account="verified_test@test.com",
        is_verified=True,
    ),
    AccountSchema(
        id=uuid4(),
        account="verified_user_test@test.com",
        is_verified=True,
    ),
    AccountSchema(
        id=uuid4(),
        account="unverified_user_test@test.com",
        is_verified=False,
    )
]
