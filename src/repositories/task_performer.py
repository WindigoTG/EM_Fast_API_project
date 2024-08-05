from typing import Any, List

from sqlalchemy import delete

from src.models import TaskPerformer
from src.utils.repository import SqlAlchemyRepository


class TaskPerformerRepository(SqlAlchemyRepository):
    model = TaskPerformer

    async def delete_multiple(
        self,
        task_id,
        performer_ids: List[Any]
    ) -> None:
        query = delete(self.model).filter_by(task_id=task_id).where(
            TaskPerformer.user_id.in_(performer_ids)
        )
        await self.session.execute(query)
