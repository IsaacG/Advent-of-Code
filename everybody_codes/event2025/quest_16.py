"""Everyone Codes Day N."""

import math
from lib import helpers
from lib import parsers


def solve(part: int, data: list[list[int]]) -> int:
    """Solve the parts."""
    cols = data[0]
    if part == 1:
        return sum(90 // i for i in cols)

    # Reverse build the wall into the spell steps.
    spell = []
    cols = data[0]
    while any(cols):
        i = next(i for i, v in enumerate(cols) if v)
        for j in range(i, len(cols), i + 1):
            cols[j] -= 1
        spell.append(i + 1)
    if part == 2:
        return math.prod(spell)

    target = 202520252025000
    # Exponentially search for the upper bound.
    high = 100
    while sum(high // i for i in spell) < target:
        high *= 2
    # Binary search for the result.
    low = high // 2
    while low + 1 < high:
        mid = (high + low) // 2
        got = sum(mid // i for i in spell)
        if got == target:
            high = mid
        elif got > target:
            high = mid - 1
        else:
            low = mid
    return high


PARSER = parsers.parse_ints
TESTS = [
    (1, "1,2,3,5,9", 193),
    (2, "1,2,2,2,2,3,1,2,3,3,1,3,1,2,3,2,1,4,1,3,2,2,1,3,2,2", 270),
    (3, "1,2,2,2,2,3,1,2,3,3,1,3,1,2,3,2,1,4,1,3,2,2,1,3,2,2", 94439495762954),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
