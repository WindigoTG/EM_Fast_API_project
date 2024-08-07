from typing import Any
from uuid import uuid4

from src.schemas.responses import BaseResponse
from src.structure.schemas.division_position import DivisionPositionSchema
from src.structure.schemas.position import PositionSchema
from src.structure.schemas.responses import (
    DivisionPositionCreateResponse,
    PositionCreateResponse,
    PositionResponse, DivisionPositionResponse,
)
from src.utils.response_factory import ResponseFactory
from src.utils.unit_of_work import UnitOfWork


class PositionService:
    @classmethod
    async def create_position(
        cls,
        uow: UnitOfWork,
        title: str
    ) -> Any:
        async with uow:
            new_position = (
                await uow.repositories["position"].add_one_and_get_obj(
                    title=title
                )
            )

        return PositionCreateResponse(
            data=PositionSchema.model_validate(new_position),
        )

    @classmethod
    async def get_position(
        cls,
        uow: UnitOfWork,
        position_id: uuid4,
    ) -> Any:
        async with uow:
            position = (
                await uow.repositories["position"].get_by_query_one_or_none(
                    id=position_id,
                )
            )
        if not position:
            return ResponseFactory.get_not_found_response(
                "Position not found"
            )

        return PositionResponse(
            data=PositionSchema.model_validate(position),
        )

    @classmethod
    async def update_position_by_id(
        cls,
        uow: UnitOfWork,
        position_id: uuid4,
        updated_data: dict,
    ) -> Any:
        async with uow:
            updated_position = (
                await uow.repositories["position"].update_one_by_id(
                    _id=position_id,
                    values=updated_data,
                )
            )
        if not updated_position:
            return ResponseFactory.get_not_found_response(
                "Position not found"
            )

        return PositionResponse(
            data=PositionSchema.model_validate(updated_position),
        )

    @classmethod
    async def delete_position(
        cls,
        uow: UnitOfWork,
        position_id: uuid4,
    ):
        async with uow:
            await uow.repositories["position"].delete_by_query(
                id=position_id,
            )
        return BaseResponse()

    @classmethod
    async def assign_position_to_division(
        cls,
        uow: UnitOfWork,
        position_id: uuid4,
        division_id: int,
        role: str,
    ) -> Any:
        async with uow:
            div_pos = (
                await uow.repositories[
                    "division_position"
                ].add_one_and_get_obj(
                    position_id=position_id,
                    division_id=division_id,
                    role=role,
                )
            )

        if not div_pos:
            return ResponseFactory.get_base_error_response("Bad request")

        return DivisionPositionCreateResponse(
            data=DivisionPositionSchema.model_validate(div_pos)
        )

    @classmethod
    async def remove_position_from_division(
        cls,
        uow: UnitOfWork,
        div_pos_id: uuid4,
    ) -> Any:
        async with uow:
            await uow.repositories["division_position"].delete_by_query(
                id=div_pos_id,
            )
        return BaseResponse()

    @classmethod
    async def update_division_position(
        cls,
        uow: UnitOfWork,
        div_pos_id: uuid4,
        updated_data: dict,
    ) -> Any:
        async with uow:
            updated_div_pos = (
                await uow.repositories["division_position"].update_one_by_id(
                    _id=div_pos_id,
                    values=updated_data,
                )
            )

        if not updated_div_pos:
            return ResponseFactory.get_not_found_response(
                "Division position not found"
            )

        return DivisionPositionResponse(
            data=DivisionPositionSchema.model_validate(updated_div_pos)
        )

    @classmethod
    async def get_division_position(
        cls,
        uow: UnitOfWork,
        div_pos_id: uuid4,
    ) -> Any:
        async with uow:
            div_pos = (
                await uow.repositories[
                    "division_position"
                ].get_by_query_one_or_none(
                    id=div_pos_id,
                )
            )
        if not div_pos:
            return ResponseFactory.get_not_found_response(
                "Division position not found"
            )

        return DivisionPositionResponse(
            data=DivisionPositionSchema.model_validate(div_pos)
        )
