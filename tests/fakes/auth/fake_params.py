from contextlib import nullcontext as does_not_raise
from uuid import uuid4

from src.auth.utils.enums import RegistrationServiceResultEnum
from tests.fakes.auth.fake_companies import FAKE_COMPANIES


# kwargs, expected_result, expectation
TEST_CHECK_IF_ACCOUNT_AVAILABLE_PARAMS = [
    ({"account": "verified_test@test.com"}, False, does_not_raise()),
    ({"account": "non_existent@test.com"}, True, does_not_raise()),
]

# kwargs, expected_result, expectation
TEST_CREATE_ACCOUNT_PARAMS = [
    (
        {"account": "verified_test@test.com"},
        RegistrationServiceResultEnum.ACCOUNT_ALREADY_EXISTS,
        does_not_raise(),
    ),
    (
        {"account": "new_account@test.com"},
        RegistrationServiceResultEnum.SUCCESS,
        does_not_raise(),
    ),
]

# kwargs, expected_result, expectation
TEST_VERIFY_ACCOUNT_PARAMS = [
    (
        {"account": "unverified_test@test.com", "invite_token": 1234},
        RegistrationServiceResultEnum.SUCCESS,
        does_not_raise(),
    ),
    (
        {"account": "verified_test@test.com", "invite_token": 5678},
        RegistrationServiceResultEnum.ACCOUNT_ALREADY_VERIFIED,
        does_not_raise(),
    ),
    (
        {"account": "nonexistent_test@test.com", "invite_token": 1234},
        RegistrationServiceResultEnum.ACCOUNT_DOES_NOT_EXIST,
        does_not_raise(),
    ),
    (
        {"account": "unverified_test@test.com", "invite_token": 5678},
        RegistrationServiceResultEnum.WRONG_TOKEN,
        does_not_raise(),
    ),
]

# kwargs, expected_result, expectation
TEST_CREATE_USER_AND_COMPANY_PARAMS = [
    (
        {
            "account": "verified_test@test.com",
            "first_name": "Petr",
            "last_name": "Petrov",
            "password": "P4s$w0rd",
            "company_name": "New Test Company",
        },
        RegistrationServiceResultEnum.SUCCESS,
        does_not_raise(),
    ),
    (
        {
            "account": "unverified_test@test.com",
            "first_name": "Petr",
            "last_name": "Petrov",
            "password": "P4s$w0rd",
            "company_name": "New Test Company",
        },
        RegistrationServiceResultEnum.ACCOUNT_NOT_VERIFIED,
        does_not_raise(),
    ),
    (
        {
            "account": "verified_user_test@test.com",
            "first_name": "Petr",
            "last_name": "Petrov",
            "password": "P4s$w0rd",
            "company_name": "New Test Company",
        },
        RegistrationServiceResultEnum.ACCOUNT_IN_USE,
        does_not_raise(),
    ),
    (
        {
            "account": "nonexistent_test@test.com",
            "first_name": "Petr",
            "last_name": "Petrov",
            "password": "P4s$w0rd",
            "company_name": "New Test Company",
        },
        RegistrationServiceResultEnum.ACCOUNT_DOES_NOT_EXIST,
        does_not_raise(),
    ),
]

# kwargs, expected_result, expectation
TEST_CREATE_ACCOUNT_AND_USER_FOR_COMPANY_PARAMS = [
    (
        {
            "account": "new_account@test.com",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "company_id": FAKE_COMPANIES[0].id,
        },
        RegistrationServiceResultEnum.SUCCESS,
        does_not_raise(),
    ),
    (
        {
            "account": "verified_test@test.com",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "company_id": FAKE_COMPANIES[0].id,
        },
        RegistrationServiceResultEnum.ACCOUNT_ALREADY_EXISTS,
        does_not_raise(),
    ),
    (
        {
            "account": "new_account@test.com",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "company_id": uuid4(),
        },
        RegistrationServiceResultEnum.COMPANY_DOES_NOT_EXIST,
        does_not_raise(),
    ),
]
