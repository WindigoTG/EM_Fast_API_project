from typing import List

from sqlalchemy import func, Sequence, Integer
from sqlalchemy.orm import foreign, Mapped, mapped_column, relationship, remote

from src.database.db import async_engine
from src.models.base import BaseModel
from src.models.custom_types import str_50_T
from sqlalchemy_utils import Ltree, LtreeType


id_seq = Sequence('division_id_seq')


class Division(BaseModel):
    __tablename__ = "division"

    id: Mapped[int] = mapped_column(Integer, id_seq, primary_key=True)
    name: Mapped[str_50_T]
    path: Mapped[Ltree] = mapped_column(LtreeType)
    parent = relationship(
        "Division",
        primaryjoin=remote(path) == foreign(func.subpath(path, 0, -1)),
        backref="children",
        viewonly=True,
    )

    positions: Mapped[List["DivisionPosition"]] = relationship(
        back_populates="division"
    )

    def __init__(self, name, parent=None):
        _id = async_engine.sync_engine.execute(id_seq)
        self.id = _id
        self.name = name
        ltree_id = Ltree(str(_id))
        self.path = ltree_id if parent is None else parent.path + ltree_id
