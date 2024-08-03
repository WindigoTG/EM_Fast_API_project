from src.models import TaskUser
from src.utils.repository import SqlAlchemyRepository


class TaskUserRepository(SqlAlchemyRepository):
    model = TaskUser
