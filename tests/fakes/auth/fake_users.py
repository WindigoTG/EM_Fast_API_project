from uuid import uuid4

from src.auth.schemas.user import UserSchema
from tests.fakes.auth.fake_companies import FAKE_COMPANIES


FAKE_USERS: list[UserSchema] = [
    UserSchema(
        id=uuid4(),
        first_name="Test",
        last_name="Testov",
        is_admin=True,
        company_id=FAKE_COMPANIES[0].id,
    ),
    UserSchema(
        id=uuid4(),
        first_name="Ivan",
        last_name="Ivanov",
        is_admin=False,
        company_id=FAKE_COMPANIES[0].id,
    ),
]
