from enum import Enum


class DivisionServiceOperationResult(Enum):
    SUCCESS = 0
    INCORRECT_PARENT = 1
    DIVISION_NOT_FOUND = 2


class RoleEnum(Enum):
    employee = 0
    manager = 1
