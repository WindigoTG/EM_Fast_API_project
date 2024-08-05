from enum import StrEnum
from typing import List
from uuid import uuid4

from fastapi import status
from fastapi.responses import JSONResponse

from src.models import Task, User
from src.schemas.responses import BaseResponse
from src.tasks.schemas.responses import TaskCreateResponse, TaskResponse
from src.tasks.schemas.task import (
    CreateTaskSchema,
    TaskSchema,
    UpdateTaskSchema,
)
from src.utils.response_factory import ResponseFactory
from src.utils.service import BaseService
from src.utils.unit_of_work import UnitOfWork


class TaskService(BaseService):
    base_repository = "task"

    class RelatedEnum(StrEnum):
        OBSERVER = "task_observer"
        PERFORMER = "task_performer"

    @classmethod
    async def create_task(
        cls,
        uow: UnitOfWork,
        author: User,
        task_data: CreateTaskSchema,
    ):
        async with uow:
            new_task = await uow.repositories["task"].add_one_and_get_obj(
                title=task_data.title,
                description=task_data.description,
                author_id=author.id,
                approver_id=task_data.approver_id,
                deadline=task_data.deadline.replace(tzinfo=None),
            )

            await cls._add_observers_and_performers_to_task(
                uow,
                task_data.observers,
                task_data.performers,
                new_task,
            )

            return JSONResponse(
                content=TaskCreateResponse(
                    data=TaskSchema.model_validate(new_task)
                ),
                status_code=status.HTTP_201_CREATED
            )

    @classmethod
    async def update_task(
        cls,
        uow: UnitOfWork,
        task_id: uuid4,
        task_data: UpdateTaskSchema,
    ):
        async with uow:
            values = {
                key: value
                for key, value in task_data.model_dump().items()
                if not (value is None or isinstance(value, list))
            }
            task = await uow.repositories["task"].update_one_by_id(
                _id=task_id,
                values=values,
            )

            if not task:
                return ResponseFactory.get_not_found_response(
                    reason="Task not found."
                )
            existing_observers = set([obs.id for obs in task.observers])
            existing_performers = set([perf.id for perf in task.performers])
            updated_observers = set(task_data.observers)
            updated_performers = set(task_data.performers)

            observers_to_add = updated_observers - existing_observers
            observers_to_remove = existing_observers - updated_observers
            performers_to_add = updated_performers - existing_performers
            performers_to_remove = existing_performers - updated_performers

            await cls._remove_observers_and_performers_from_task(
                uow,
                observers_to_remove,
                performers_to_remove,
                task,
            )

            await cls._add_observers_and_performers_to_task(
                uow,
                observers_to_add,
                performers_to_add,
                task,
            )

            if any(
                [
                    observers_to_add,
                    observers_to_remove,
                    performers_to_remove,
                    performers_to_add
                ]
            ):
                await uow.refresh_object(task)

            return TaskResponse(data=TaskSchema.model_validate(task))

    @classmethod
    async def get_task(
        cls,
        uow: UnitOfWork,
        task_id: uuid4,
    ):
        async with uow:
            task = await uow.repositories["task"].get_by_query_one_or_none(
                id=task_id
            )

            if not task:
                return ResponseFactory.get_not_found_response(
                    reason="Task not found."
                )

            return TaskResponse(data=TaskSchema.model_validate(task))

    @classmethod
    async def delete_task(
        cls,
        uow: UnitOfWork,
        task_id: uuid4,
        user: User,
    ):
        async with uow:
            task = await uow.repositories["task"].get_by_query_one_or_none(
                id=task_id
            )

            if not task:
                return ResponseFactory.get_not_found_response(
                    reason="Task not found.",
                )

            if task.author_id != user.id:
                return ResponseFactory.get_base_error_response(
                    reason='Only the author can delete task.',
                )

            await uow.repositories["task"].delete_by_query(id=task_id)

            return BaseResponse()

    @classmethod
    async def _add_observers_and_performers_to_task(
        cls,
        uow: UnitOfWork,
        observers: List[uuid4],
        performers: List[uuid4],
        task: Task,
    ):
        if observers:
            await cls._add_users_to_task(
                uow,
                task,
                cls.RelatedEnum.OBSERVER,
                observers,
            )
        if performers:
            await cls._add_users_to_task(
                uow,
                task,
                cls.RelatedEnum.PERFORMER,
                performers,
            )

    @classmethod
    async def _add_users_to_task(
        cls,
        uow: UnitOfWork,
        task: Task,
        rel: RelatedEnum,
        users: List[uuid4],
    ):
        await uow.repositories[rel.value].add_multiple(
            [
                {"task_id": task.id, "user_id": user_id}
                for user_id in users
            ]
        )

    @classmethod
    async def _remove_observers_and_performers_from_task(
            cls,
            uow: UnitOfWork,
            observers: List[uuid4],
            performers: List[uuid4],
            task: Task,
    ):
        if observers:
            await cls._remove_users_from_task(
                uow,
                task,
                cls.RelatedEnum.OBSERVER,
                observers,
            )
        if performers:
            await cls._remove_users_from_task(
                uow,
                task,
                cls.RelatedEnum.PERFORMER,
                performers,
            )

    @classmethod
    async def _remove_users_from_task(
        cls,
        uow: UnitOfWork,
        task: Task,
        rel: RelatedEnum,
        users: List[uuid4],
    ):
        await uow.repositories[rel.value].delete_multiple(
            task.id,
            users,
        )
