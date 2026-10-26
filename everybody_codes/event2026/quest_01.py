"""Everyone Codes Event 2026 Day 1."""

import itertools
from lib import helpers


def solve(part: int, data: list[int]) -> int:
    """Solve the parts."""
    need = 0
    for have in data:
        if part == 1:
            want = next(i * i for i in itertools.count(1) if i * i >= have)
        elif part == 2:
            want = next(4 * i for i in itertools.count(2) if 4 * i >= have)
        else:
            want = next(i * i - 1 for i in itertools.count(3, 2) if i * i - 1 >= have)
        need += want - have
    return need


TEST_DATA = "3,11,12,16,24,25"
TESTS = [
    (1, TEST_DATA, 11),
    (2, TEST_DATA, 9),
    (3, TEST_DATA, 61),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
