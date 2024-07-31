from src.auth.models import Secret
from src.utils.repository import SqlAlchemyRepository


class SecretRepository(SqlAlchemyRepository):
    model = Secret
