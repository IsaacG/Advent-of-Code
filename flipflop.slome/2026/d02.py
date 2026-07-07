"""FlipFlop Codes: N."""

import logging
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part == 1:
        p = 0

        t = [0] * 100
        for i in data:
            p += 1 if i == ">" else -1
            p %= 100
            t[p] += 1
        m = max(t)
        return m * (t.index(m) + 1)
    if part == 2:
        r = 0
        w = 0
        heat = 0
        for a, b in zip(data, reversed(data)):
            r += 1 if a == ">" else -1
            w += 1 if b == ">" else -1
            if r == w:
                heat += 1
        return heat
    if part == 3:
        r = 0
        t = [0] * 100
        for a, b in zip(data, reversed(data)):
            r += 1 if a == ">" else -1
            r -= 1 if b == ">" else -1
            r %= 100
            t[r] += 1
        m = max(t)
        return m * (t.index(m) + 1)


# PARSER = parsers.parse_one_str
TEST_DATA = [
    "><>><<>><<<>>>>><><><><><>>>>>"
]
TESTS = [
    (1, TEST_DATA[0], 12),
    (2, TEST_DATA[0], 3),
    (3, TEST_DATA[0], 1358),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
