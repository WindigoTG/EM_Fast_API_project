from enum import StrEnum


class TaskStatusEnum(StrEnum):
    pending = "сделать"
    ongoing = "в работе"
    done = "сделано"
    cancelled = "отменено"
