from enum import Enum, StrEnum


class RegistrationServiceResultEnum(Enum):
    SUCCESS = 0
    ACCOUNT_DOES_NOT_EXIST = 1
    ACCOUNT_ALREADY_EXISTS = 2
    ACCOUNT_NOT_VERIFIED = 3
    ACCOUNT_ALREADY_VERIFIED = 4
    ACCOUNT_IN_USE = 5
    WRONG_TOKEN = 6
    COMPANY_DOES_NOT_EXIST = 7
    NOT_ALLOWED = 8,
    USER_NOT_CREATED = 9,


class TokenTypeEnum(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"
