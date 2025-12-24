#!/bin/python
"""Advent of Code, Day 5: Cafeteria."""
from lib import aoc


def solve(data: list[list[list[int]]], part: int) -> int:
    """Return how many fresh ingredients there are."""
    fresh, available = data
    fresh.sort()
    if part == 1:
        return sum(
            any(x <= ingredient <= y for x, y in fresh)
            for ingredient in available
        )

    opened, closed = fresh[0]
    total = 0
    for start, end in fresh[1:]:
        if start > closed:
            total += 1 + closed - opened
            opened, closed = start, end
        else:
            closed = max(closed, end)
    total += 1 + closed - opened
    return total


SAMPLE = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
TESTS = [(1, SAMPLE, 3), (2, SAMPLE, 14)]
# vim:expandtab:sw=4:ts=4
