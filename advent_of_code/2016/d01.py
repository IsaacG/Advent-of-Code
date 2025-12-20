#!/bin/python
"""Advent of Code, Day 1: No Time for a Taxicab. Compute how far we travelled."""

from lib import aoc


def solve(data: list[list[str]], part: int) -> int:
    """Compute how far we walked."""
    cur = complex(0, 0)
    seen = {cur}
    heading = complex(0, 1)

    for instruction in data[0]:
        rot, dist = instruction[0], int(instruction[1:])
        heading *= {"R": -1j, "L": +1j}[rot]
        for _ in range(dist):
            cur += heading
            if part == 2 and cur in seen:
                return int(abs(cur.real) + abs(cur.imag))
            seen.add(cur)

    return int(abs(cur.real) + abs(cur.imag))


PARSER = aoc.parse_re_findall_str(r"[LR]\d+")
TESTS = [
    (1, 'R2, L3', 5),
    (1, 'R2, R2, R2', 2),
    (1, 'R5, L5, R5, R3', 12),
    (2, 'R8, R4, R4, R8', 4),
]
