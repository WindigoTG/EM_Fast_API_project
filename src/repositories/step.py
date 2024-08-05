from src.models import Step
from src.utils.repository import SqlAlchemyRepository


class StepRepository(SqlAlchemyRepository):
    model = Step
