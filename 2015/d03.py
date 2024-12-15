#!/bin/python
"""Advent of Code: Day 03."""

from collections.abc import Callable

from lib import aoc

SAMPLE = ["^>v<", "^v^v^v^v^v"]
InputType = list[str]
MAPPING = aoc.ARROW_DIRECTIONS


class Day03(aoc.Challenge):
    """Day 3: Perfectly Spherical Houses in a Vacuum. Track which houses get presents."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=4),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=2),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=3),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=11),
    ]

    def solver(self, line: str, part_one: bool) -> int:
        """Return how many houses get presents."""
        pos = {True: complex(0), False: complex(0)}
        robot = False
        visited = {pos[robot]}
        for char in line:
            pos[robot] += MAPPING[char]
            visited.add(pos[robot])
            if not part_one:
                robot = not robot
        return len(visited)
