from uuid import uuid4

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from schemas.responses import BaseResponse
from src.tasks.schemas.responses import StepCreateResponse, StepResponse
from src.tasks.schemas.step import (
    CreateStepSchema,
    StepSchema,
    UpdateStepSchema,
)
from src.utils.response_factory import ResponseFactory
from src.utils.service import BaseService
from src.utils.unit_of_work import UnitOfWork


class StepService(BaseService):
    base_repository = "step"

    @classmethod
    async def create_step(
            cls,
            uow: UnitOfWork,
            step_data: CreateStepSchema,
    ):
        async with uow:
            try:
                new_step = await uow.repositories[
                    cls.base_repository
                ].add_one_and_get_obj(
                    **step_data.model_dump()
                )
            except IntegrityError:
                return ResponseFactory.get_base_error_response(
                    "Unable to create step."
                )

            return StepCreateResponse(
                    data=StepSchema.model_validate(new_step)
                )

    @classmethod
    async def update_step(
        cls,
        uow: UnitOfWork,
        step_id: uuid4,
        step_data: UpdateStepSchema,
    ):
        async with uow:
            step = await uow.repositories[
                cls.base_repository
            ].update_one_by_id(_id=step_id, values=step_data.model_dump())

            if not step:
                return ResponseFactory.get_not_found_response(
                    reason="Step not found."
                )

            return StepResponse(data=StepSchema.model_validate(step))

    @classmethod
    async def get_step(
            cls,
            uow: UnitOfWork,
            step_id: uuid4,
    ):
        async with uow:
            step = await uow.repositories[
                cls.base_repository
            ].get_by_query_one_or_none(id=step_id)

            if not step:
                return ResponseFactory.get_not_found_response(
                    reason="Step not found."
                )

            return StepResponse(data=StepSchema.model_validate(step))

    @classmethod
    async def delete_step(
            cls,
            uow: UnitOfWork,
            step_id: uuid4,
    ):
        async with uow:
            await uow.repositories[
                cls.base_repository
            ].delete_by_query(id=step_id)

            return BaseResponse()
