from src.auth.schemas.secret import SecretSchema
from tests.fakes.auth.fake_accounts import FAKE_ACCOUNTS
from tests.fakes.auth.fake_users import FAKE_USERS


FAKE_SECRETS: list[SecretSchema] = [
    SecretSchema(
        account_id=FAKE_ACCOUNTS[2].id,
        user_id=FAKE_USERS[0].id,
        hashed_password="03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"
    ),
    # SecretSchema(
    #     account_id=FAKE_ACCOUNTS[3].id,
    #     user_id=FAKE_USERS[1].id,
    #     hashed_password=""
    # ),
]
