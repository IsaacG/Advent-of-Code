#!/bin/python
"""Advent of Code, Day 8: Matchsticks. Escape and un-escape strings."""
from lib import aoc


def solve(data: list[str], part: int) -> int:
    """Return the length of escaping chars compared to decoded/encoded version."""
    if part == 1:
        return sum(len(a) - len(eval(a)) for a in data)
    return sum(2 + a.count('"') + a.count("\\") for a in data)


SAMPLE = ['""', '"abc"', r'"aaa\"aaa"', r'"\x27"']
TESTS = [
    (1, SAMPLE[0], 2),
    (1, SAMPLE[1], 2),
    (1, SAMPLE[2], 3),
    (1, SAMPLE[3], 5),
    (2, SAMPLE[0], 4),
    (2, SAMPLE[1], 4),
    (2, SAMPLE[2], 6),
    (2, SAMPLE[3], 5),
]

