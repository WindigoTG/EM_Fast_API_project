from uuid import uuid4

from src.auth.schemas.company import CompanySchema


FAKE_COMPANIES: list[CompanySchema] = [
    CompanySchema(
        id=uuid4(),
        name="Test_company_1",
        description="",
    ),
]
