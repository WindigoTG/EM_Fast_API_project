from typing import Optional
from uuid import uuid4

from src.structure.models import DivisionPosition, Position
from src.structure.units_of_work.position import PositionUnitOfWork


class PositionService:
    @classmethod
    async def create_position(
        cls,
        uow: PositionUnitOfWork,
        title: str
    ) -> Position:
        async with uow:
            new_position = (
                await uow.repositories["position"].add_one_and_get_obj(
                    title=title
                )
            )
        return new_position

    @classmethod
    async def get_position(
        cls,
        uow: PositionUnitOfWork,
        position_id: uuid4,
    ) -> Optional[Position]:
        async with uow:
            position = (
                await uow.repositories["position"].get_by_query_one_or_none(
                    id=position_id,
                )
            )
        return position

    @classmethod
    async def update_position_by_id(
        cls,
        uow: PositionUnitOfWork,
        position_id: uuid4,
        updated_data: dict,
    ):
        async with uow:
            updated_position = (
                await uow.repositories["position"].update_one_by_id(
                    _id=position_id,
                    values=updated_data,
                )
            )

        return updated_position

    @classmethod
    async def delete_position(
        cls,
        uow: PositionUnitOfWork,
        position_id: uuid4,
    ):
        async with uow:
            await uow.repositories["position"].delete_by_query(
                id=position_id,
            )

    @classmethod
    async def assign_position_to_division(
        cls,
        uow: PositionUnitOfWork,
        position_id: uuid4,
        division_id: int,
        role: str,
    ) -> DivisionPosition:
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

        return div_pos

    @classmethod
    async def remove_position_from_division(
        cls,
        uow: PositionUnitOfWork,
        div_pos_id: uuid4,
    ) -> DivisionPosition:
        async with uow:
            await uow.repositories["division_position"].delete_by_query(
                id=div_pos_id,
            )

    @classmethod
    async def update_division_position(
        cls,
        uow: PositionUnitOfWork,
        div_pos_id: uuid4,
        updated_data: dict,
    ) -> DivisionPosition:
        async with uow:
            updated_div_pos = (
                await uow.repositories["division_position"].update_one_by_id(
                    _id=div_pos_id,
                    values=updated_data,
                )
            )

        return updated_div_pos

    @classmethod
    async def get_division_position(
        cls,
        uow: PositionUnitOfWork,
        div_pos_id: uuid4,
    ) -> Optional[DivisionPosition]:
        async with uow:
            div_pos = (
                await uow.repositories[
                    "division_position"
                ].get_by_query_one_or_none(
                    id=div_pos_id,
                )
            )
        return div_pos
