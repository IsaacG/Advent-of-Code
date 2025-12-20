#!/bin/python
"""Advent of Code, Day 3: Perfectly Spherical Houses in a Vacuum. Track which houses get presents."""

from lib import aoc
MAPPING = aoc.ARROW_DIRECTIONS


def solve(data: str, part: int) -> int:
    """Return how many houses get presents."""
    pos = {True: complex(0), False: complex(0)}
    robot = False
    visited = {pos[robot]}
    for char in data:
        pos[robot] += MAPPING[char]
        visited.add(pos[robot])
        if part == 2:
            robot = not robot

    return len(visited)


SAMPLE = ["^>v<", "^v^v^v^v^v"]
TESTS = [
    (1, SAMPLE[0], 4),
    (1, SAMPLE[1], 2),
    (2, SAMPLE[0], 3),
    (2, SAMPLE[1], 11),
]
