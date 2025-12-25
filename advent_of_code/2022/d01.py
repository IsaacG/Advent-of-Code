#!/bin/python
"""Advent of Code: Day 01. Count how many calories the elves have."""


def solve(data: list[list[int]], part: int) -> int:
    """Return the sum calories held by the elf(s) with the most calories."""
    calories = sorted((sum(i) for i in data), reverse=True)
    return sum(calories[:1 if part == 1 else 3])


SAMPLE = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""
TESTS = [(1, SAMPLE, 24000), (2, SAMPLE, 45000)]
