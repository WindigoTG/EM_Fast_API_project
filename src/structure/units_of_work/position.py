from src.utils.unit_of_work import UnitOfWork


from src.auth.repositories import UserRepository
from src.structure.repositories import (
    DivisionRepository,
    DivisionPositionRepository,
    PositionRepository,
)


class PositionUnitOfWork(UnitOfWork):
    async def __aenter__(self):
        self.session = self.session_factory()
        self.repositories = {
            "division": DivisionRepository(self.session),
            "division_position": DivisionPositionRepository(self.session),
            "position": PositionRepository(self.session),
            "user": UserRepository(self.session),
        }
