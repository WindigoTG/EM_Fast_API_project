from src.utils.unit_of_work import UnitOfWork


from src.auth.repositories import (
    AccountRepository,
    CompanyRepository,
    InviteRepository,
    SecretRepository,
    UserRepository,
)


class AuthUnitOfWork(UnitOfWork):
    async def __aenter__(self):
        self.session = self.session_factory()
        self.repositories = {
            "account": AccountRepository(self.session),
            "company": CompanyRepository(self.session),
            "invite": InviteRepository(self.session),
            "secret": SecretRepository(self.session),
            "user": UserRepository(self.session),
        }
