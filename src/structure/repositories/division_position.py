from src.models import DivisionPosition
from src.utils.repository import SqlAlchemyRepository


class DivisionPositionRepository(SqlAlchemyRepository):
    model = DivisionPosition
