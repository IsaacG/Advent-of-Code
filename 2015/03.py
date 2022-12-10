#!/bin/python
"""Advent of Code: Day 03."""

from typing import Callable

import typer
from lib import aoc

SAMPLE = ["^>v<", "^v^v^v^v^v"]
InputType = list[str]
MAPPING = {
    "^": complex(0, +1),
    "v": complex(0, -1),
    "<": complex(-1, 0),
    ">": complex(+1, 0),
}


class Day03(aoc.Challenge):
    """Day 3: Perfectly Spherical Houses in a Vacuum. Track which houses get presents."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=4),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=2),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=3),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=11),
    )
    INPUT_PARSER = aoc.parse_one_str

    def generic(self, line: str, transform: Callable[[bool], bool]) -> int:
        """Return how many houses get presents."""
        pos = {True: complex(0), False: complex(0)}
        robot = False
        visited = {pos[robot]}
        for char in line:
            pos[robot] += MAPPING[char]
            visited.add(pos[robot])
            robot = transform(robot)
        return len(visited)

    def part1(self, parsed_input: InputType) -> int:
        """Return how many houses get presents from just Santa."""
        return self.generic(parsed_input, lambda x: x)

    def part2(self, parsed_input: InputType) -> int:
        """Return how many houses get presents from Santa and Robo-Santa."""
        return self.generic(parsed_input, lambda x: not x)


if __name__ == "__main__":
    typer.run(Day03().run)

# vim:expandtab:sw=4:ts=4
