from typing import Union, Optional

from sqlalchemy import func, update

from src.models import Division
from src.models.division import id_seq
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

    async def change_path_of_descendants(
        self,
        parent_path: Ltree,
        new_parent_path: Optional[Ltree],
    ):
        parent_idx = len(parent_path)
        query = update(self.model).filter(
            self.model.path.descendant_of(parent_path)
        ).values(
            path=(
                func.text2ltree(new_parent_path.path).op('||')(
                    func.subpath(self.model.path, parent_idx)
                )
                if parent_idx > 1
                else func.subpath(self.model.path, parent_idx)
            )
        )
        await self.session.execute(query)
