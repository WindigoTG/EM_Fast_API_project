from typing import Union, Any

from sqlalchemy_utils import Ltree

from src.structure.utils.enums import DivisionServiceOperationResult
from src.utils.service import BaseService
from src.utils.unit_of_work import UnitOfWork


class DivisionService(BaseService):
    base_repository = "division"

    @classmethod
    async def update_one_by_id(
            cls,
            uow: UnitOfWork,
            _id: Union[int, str],
            values: dict
    ) -> tuple[DivisionServiceOperationResult, Any]:
        updated_data = values.copy()

        try:
            parent_path = updated_data.pop("parent_path")
        except KeyError:
            parent_path = None

        try:
            parent_id = updated_data.pop("parent_id")
        except KeyError:
            parent_id = None

        async with uow:
            parent = None
            if parent_path:
                parent = await uow.__dict__[
                    cls.base_repository
                ].get_by_query_one_or_none(path=Ltree(parent_path))

            if not parent and parent_id:
                parent = await uow.__dict__[
                    cls.base_repository
                ].get_by_query_one_or_none(id=parent_id)

            if not parent and (parent_path or parent_id):
                return DivisionServiceOperationResult.INCORRECT_PARENT, None

            div_path = Ltree(str(_id))
            new_path = parent.path + div_path if parent else div_path

            if new_path != div_path and new_path.ancestor_of(div_path):
                return DivisionServiceOperationResult.INCORRECT_PARENT, None

            if parent:
                updated_data["path"] = new_path

            _obj = await uow.__dict__[cls.base_repository].update_one_by_id(
                _id=_id,
                values=updated_data,
            )

            if not _obj:
                return (
                    DivisionServiceOperationResult.DIVISION_NOT_FOUND,
                    None
                )

            return DivisionServiceOperationResult.SUCCESS, _obj
