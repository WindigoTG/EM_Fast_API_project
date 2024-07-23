from uuid import uuid4

from src.auth.schemas.invite import InviteSchema
from tests.fakes.auth.fake_accounts import FAKE_ACCOUNTS

FAKE_INVITES = [
    InviteSchema(
        id=uuid4(),
        token=1234,
        account_id=FAKE_ACCOUNTS[0].id,
    ),
    InviteSchema(
        id=uuid4(),
        token=5678,
        account_id=FAKE_ACCOUNTS[1].id,
    )
]
