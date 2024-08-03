from src.models import Task
from src.utils.repository import SqlAlchemyRepository


class TaskRepository(SqlAlchemyRepository):
    model = Task
