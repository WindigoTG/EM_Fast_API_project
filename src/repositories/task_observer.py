from typing import Any, List

from sqlalchemy import delete

from src.models import TaskObserver
from src.utils.repository import SqlAlchemyRepository


class TaskObserverRepository(SqlAlchemyRepository):
    model = TaskObserver

    async def delete_multiple(
        self,
        task_id,
        observer_ids: List[Any]
    ) -> None:
        query = delete(self.model).filter_by(task_id=task_id).where(
            TaskObserver.user_id.in_(observer_ids))
        await self.session.execute(query)
