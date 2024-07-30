from typing import Union

from sqlalchemy import select
from sqlalchemy.engine import Result

from src.structure.models import Division
from src.structure.models.division import id_seq
from src.utils.repository import SqlAlchemyRepository
from sqlalchemy_utils import Ltree


class DivisionRepository(SqlAlchemyRepository):
    model = Division

    async def _new_division_kwargs(self, **kwargs):
        parent = kwargs.get('parent')
        _id = await self.session.execute(id_seq)
        kwargs['id'] = _id
        ltree_id = Ltree(str(_id))
        kwargs['path'] = ltree_id if parent is None else parent.path + ltree_id
        return kwargs

    async def add_one(self, **kwargs) -> None:
        _kwargs = await self._new_division_kwargs(**kwargs)
        await super().add_one(**_kwargs)

    async def add_one_and_get_id(self, **kwargs) -> Union[int, str]:
        _kwargs = await self._new_division_kwargs(**kwargs)
        _id = await super().add_one_and_get_id(**_kwargs)
        return _id

    async def add_one_and_get_obj(self, **kwargs) -> type(model):
        _kwargs = await self._new_division_kwargs(**kwargs)
        _obj = await super().add_one_and_get_obj(**_kwargs)
        return _obj

    async def reset_path(self, parent_path: str):
        query = select(self.model).filter(
            self.model.path.descendant_of(Ltree(parent_path)),
        )
        res: Result = await self.session.execute(query)
        descendants_to_reset = res.scalars().all()
        for descendant in descendants_to_reset:
            descendant.path = Ltree(str(descendant.id))
