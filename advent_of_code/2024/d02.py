#!/bin/python
"""Advent of Code, Day 2: Red-Nosed Reports."""

from lib import aoc

def safe(line: list[int]) -> bool:
    """Return if a report is safe."""
    return all(
        0 < abs(a - b) <= 3
        for a, b in zip(line, line[1:])
    ) and all(
        (a < b) == (line[0] < line[1])
        for a, b in zip(line, line[1:])
    )

def solve(data: list[list[int]], part: int) -> int:
    """Return the number of safe reports, possibly allowing one reading to be removed."""
    return sum(
        (
            safe(line)
            or any(
                safe(line[:i] + line[i + 1:])
                for i in range(0 if part == 1 else len(line))
            )
        )
        for line in data
    )


SAMPLE = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
TESTS = [(1, SAMPLE, 2), (2, SAMPLE, 4)]
# vim:expandtab:sw=4:ts=4
