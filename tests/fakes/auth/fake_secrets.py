from src.auth.schemas.secret import SecretSchema
from tests.fakes.auth.fake_accounts import FAKE_ACCOUNTS
from tests.fakes.auth.fake_users import FAKE_USERS


FAKE_SECRETS: list[SecretSchema] = [
    SecretSchema(
        account_id=FAKE_ACCOUNTS[2].id,
        user_id=FAKE_USERS[0].id,
        hashed_password=b'$2b$12$56hIzTzK8rCIT23fMtexsuBy929HRIxEF3x807EGJPI5qWm8B7h8K'
    ),
    # SecretSchema(
    #     account_id=FAKE_ACCOUNTS[3].id,
    #     user_id=FAKE_USERS[1].id,
    #     hashed_password=""
    # ),
]
