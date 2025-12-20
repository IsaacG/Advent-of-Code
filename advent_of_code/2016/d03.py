#!/bin/python
"""Advent of Code, Day 3: Squares With Three Sides. Count valid triangles."""


def solve(data: list[list[int]], part: int) -> int:
    """Return the number of valid triangles."""
    if part == 2:
        data = [
            list(row[i:i + 3])
            for row in zip(*data)
            for i in range(0, len(row), 3)
        ]
    return sum(2 * max(vals) < sum(vals) for vals in data)


TESTS = list[tuple[int, int, int]]()
