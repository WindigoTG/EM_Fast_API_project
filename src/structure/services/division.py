from typing import Union, Any

from sqlalchemy_utils import Ltree

from src.schemas.responses import BaseResponse
from src.structure.schemas.division import DivisionSchema
from src.structure.schemas.responses import (
    DivisionCreateResponse,
    DivisionResponse,
)
from src.utils.service import BaseService
from src.utils.response_factory import ResponseFactory
from src.utils.unit_of_work import UnitOfWork


class DivisionService(BaseService):
    base_repository = "division"

    @classmethod
    async def update_one_by_id(
        cls,
        uow: UnitOfWork,
        _id: Union[int, str],
        values: dict
    ) -> Any:
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
            obj_to_update = await uow.repositories[
                    cls.base_repository
                ].get_by_query_one_or_none(id=_id)

            if not obj_to_update:
                return ResponseFactory.get_not_found_response(
                    "Division does not exist."
                )
            old_path = obj_to_update.path

            parent = None
            if parent_path:
                parent = await uow.repositories[
                    cls.base_repository
                ].get_by_query_one_or_none(path=Ltree(parent_path))

            if not parent and parent_id:
                parent = await uow.repositories[
                    cls.base_repository
                ].get_by_query_one_or_none(id=parent_id)

            if not parent and (parent_path or parent_id):
                return ResponseFactory.get_base_error_response(
                    "Incorrect parent"
                )

            div_path = Ltree(str(_id))
            new_path = parent.path + div_path if parent else div_path

            if new_path != div_path and new_path.ancestor_of(div_path):
                return ResponseFactory.get_base_error_response(
                    "Incorrect parent"
                )

            updated_data["path"] = new_path

            _obj = await uow.repositories[
                cls.base_repository
            ].update_one_by_id(
                _id=_id,
                values=updated_data,
            )

            if _obj.path != old_path:
                await uow.repositories[
                    cls.base_repository
                ].change_path_of_descendants(old_path, _obj.path)

            return DivisionResponse(
                data=DivisionSchema.model_validate(_obj),
            )

    @classmethod
    async def delete_by_id(
        cls,
        uow: UnitOfWork,
        _id: Union[int, str],
    ) -> Any:
        async with uow:
            division_to_delete = await uow.repositories[
                cls.base_repository
            ].get_by_query_one_or_none(id=_id)

            if not division_to_delete:
                ResponseFactory.get_not_found_response(
                    "Division does not exist."
                )

            path = division_to_delete.path

            await uow.repositories[
                cls.base_repository
            ].delete_by_query(id=_id)

            await uow.repositories[
                cls.base_repository
            ].change_path_of_descendants(path, path[0:-1])

            return BaseResponse()

    @classmethod
    async def add_one_and_get_obj(
            cls,
            uow: UnitOfWork,
            **kwargs
    ) -> Any:
        async with uow:
            _obj = await super().add_one_and_get_obj(**kwargs)

        return DivisionCreateResponse(
            data=DivisionSchema.model_validate(_obj)
        )

    @classmethod
    async def get_by_query_one_or_none(
            cls,
            uow: UnitOfWork,
            **kwargs
    ) -> Any:
        async with uow:
            _result = await super().get_by_query_one_or_none(**kwargs)

            if _result:
                return DivisionResponse(
                    data=DivisionSchema.model_validate(_result))

            return ResponseFactory.get_not_found_response(
                "Division does not exist."
            )
