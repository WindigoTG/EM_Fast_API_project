from src.utils.unit_of_work import UnitOfWork


from src.structure.repositories.division import DivisionRepository


class DivisionUnitOfWork(UnitOfWork):
    async def __aenter__(self):
        self.session = self.session_factory()
        self.division = DivisionRepository(self.session)
        self.repositories = {
            "division": self.division,
        }
