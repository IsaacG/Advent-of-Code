"""Everyone Codes Event 2026 Day N."""

import collections
import math
import logging
from lib import helpers
from lib import parsers

log = logging.info

def seconds(growth, limit):
    t = 1
    branches = {1: 1}
    bp = 0
    while (total := bp + sum(size * num for size, num in branches.items())) < limit:
        t += 1
        n = collections.defaultdict(int)
        for size, num in branches.items():
            size += 1
            if size < growth:
                n[size] += num
            else:
                n[1] += num
                n[size // 2] += 2 * num
                bp += num
        branches = n
    return t


def seconds2(growth, limit):
    t = 1
    branches = {1: 1}
    bp = 0
    seen = {}
    jump = True
    while bp + 1 < limit:
        gf = growth - max(branches)
        t += gf
        n = collections.defaultdict(int)
        for size, num in branches.items():
            size += gf
            if size < growth:
                n[size] += num
            else:
                n[1] += num
                n[size // 2] += 2 * num
                bp += num

        branches = n
    return t


def solve(part: int, data: str, testing) -> int:
    """Solve the parts."""
    t = 0
    for plant, growth, limit in data:
        if part == 1:
            s = seconds(growth, limit)
        else:
            s = seconds2(growth, limit)
        t += s
    # p1 != 230
    if not testing and part == 1:
        assert t not in {230}
    if not testing and part == 3:
        assert len(str(t)) == len(str(817947616167071))
        assert str(t)[0] == "8"
        assert t not in {817947616167071}
    return t


# PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
""",
    """\
""",
    """\
""",
    """\
""",
    """\
""",
]
TESTS = [
    # (1, TEST_DATA[0], None),
    # (2, TEST_DATA[1], None),
    # (3, TEST_DATA[2], None),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
