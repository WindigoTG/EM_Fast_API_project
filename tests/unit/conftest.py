from copy import deepcopy
from typing import Callable, List, Sequence

import pytest
from sqlalchemy import text, Result, select, insert


@pytest.fixture(scope="session")
def compare_two_sequences() -> Callable:
    def _compare_two_sequences(first: Sequence, second: Sequence) -> bool:
        _equality_len = len(first) == len(second)
        _equality_obj = all([obj in second for obj in first])
        return all([_equality_len, _equality_obj])

    return _compare_two_sequences
