#!/bin/python
"""Advent of Code, Day 2: Corruption Checksum. Compute checksums of lines."""
from __future__ import annotations

import itertools


def solve(data: list[list[int]], part: int) -> int:
    """Return the checksum of the input lines."""
    # Return the sum difference between the largest and smallest value on each line.
    if part == 1:
        return sum(max(line) - min(line) for line in data)

    # Return the sum quotient between two evenly divisible numbers on each line.
    return sum(
        next(
            a // b
            for a, b in itertools.combinations(sorted(line, reverse=True), 2)
            if a % b == 0
        )
        for line in data
    )


SAMPLE = [
    """\
5 1 9 5
7 5 3
2 4 6 8""",
    """\
5 9 2 8
9 4 7 3
3 8 6 5""",
]
TESTS = [
    (1, SAMPLE[0], 18),
    (2, SAMPLE[1], 9),
]
# vim:expandtab:sw=4:ts=4
