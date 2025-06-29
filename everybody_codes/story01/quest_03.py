"""Everyone Codes Day N."""

import logging
import math
import re

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    steps = 100
    
    if part == 1:
        total = 0
        for line in data.splitlines():
            x, y = [int(i) for i in re.match(r"x=(.*) y=(.*)", line).groups()]
            period = x + y - 1
            final_x = (x + steps - 1) % period + 1
            final_y = (y - steps - 1) % period + 1
            total += final_x + 100 * final_y
        return total

    if part == 2 or part == 3:
        step = 1
        offset = 0
        for line in data.splitlines():
            x, y = [int(i) for i in re.match(r"x=(.*) y=(.*)", line).groups()]
            period = x + y - 1
            while (y - offset - 1) % period != 0:
                offset += step
            step = math.lcm(step, period)

        return offset


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
    # (3, TEST_DATA[2], None),
]
