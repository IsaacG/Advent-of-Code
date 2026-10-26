"""Everyone Codes Day N."""

import itertools
import logging
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    total = 0
    for n in data:
        if part == 1:
            t = next(i*i for i in itertools.count(1) if i*i >= n)
        elif part == 2:
            t = next(4*i for i in itertools.count(2) if 4*i >= n)
        else:
            t = next(i*i-1 for i in itertools.count(3, 2) if i*i-1 >= n)
        total += t - n
    return total


# PARSER = parsers.parse_one_str
TEST_DATA = [
    "3,11,12,16,24,25",
    "3,11,12,16,24,25",
    "3,11,12,16,24,25",
]
TESTS = [
    (1, TEST_DATA[0], 11),
    (2, TEST_DATA[1], 9),
    (3, TEST_DATA[2], 61),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
