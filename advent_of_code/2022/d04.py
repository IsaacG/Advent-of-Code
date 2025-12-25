#!/bin/python
"""Advent of Code: Day 04. Camp Cleanup. Detect overlapping ranges."""
from lib import aoc
PARSER = aoc.parse_re_findall_int(r"\d+")


def solve(data: list[list[int]], part: int) -> int:
    """Return the number of overlaps."""
    if part == 1:
        return sum(
            (a1 >= b1 and a2 <= b2) or (b1 >= a1 and b2 <= a2)
            for a1, a2, b1, b2 in data
        )
    return sum(
        b1 <= a1 <= b2 or a1 <= b1 <= a2
        for a1, a2, b1, b2 in data
    )


SAMPLE = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
TESTS = [(1, SAMPLE, 2), (2, SAMPLE, 4)]
