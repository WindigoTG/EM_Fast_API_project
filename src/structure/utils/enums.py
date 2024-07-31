from enum import Enum, StrEnum


class DivisionServiceOperationResult(Enum):
    SUCCESS = 0
    INCORRECT_PARENT = 1
    DIVISION_NOT_FOUND = 2


class RoleEnum(StrEnum):
    employee = "employee"
    manager = "manager"
