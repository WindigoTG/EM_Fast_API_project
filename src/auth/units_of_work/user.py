from src.utils.unit_of_work import UnitOfWork


from src.auth.repositories import (
    UserRepository,
)


class UserUnitOfWork(UnitOfWork):
    async def __aenter__(self):
        self.session = self.session_factory()
        self.repositories = {
            "user": UserRepository(self.session),
        }
