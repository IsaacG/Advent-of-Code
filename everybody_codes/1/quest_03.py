"""Everyone Codes Day N."""

import math
import re


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    snails = []
    for line in data.splitlines():
        match = re.match(r"x=(.*) y=(.*)", line)
        assert match
        x, y = [int(i) for i in match.groups()]
        period = x + y - 1
        snails.append((x, y, period))

    if part == 1:
        total = 0
        steps = 100
        for x, y, period in snails:
            final_x = (x + steps - 1) % period + 1
            final_y = (y - steps - 1) % period + 1
            total += final_x + 100 * final_y
        return total

    combined_period = 1
    days = 0
    for x, y, period in snails:
        while (y - days - 1) % period != 0:
            days += combined_period
        combined_period = math.lcm(combined_period, period)

    return days


TEST_DATA = [
    """\
x=1 y=2
x=2 y=3
x=3 y=4
x=4 y=4""",
    """\
x=12 y=2
x=8 y=4
x=7 y=1
x=1 y=5
x=1 y=3""",
    """\
x=3 y=1
x=3 y=9
x=1 y=5
x=4 y=10
x=5 y=3""",
]
TESTS = [
    (1, TEST_DATA[0], 1310),
    (2, TEST_DATA[1], 14),
    (2, TEST_DATA[2], 13659),
]
