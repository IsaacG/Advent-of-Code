#!/bin/python
"""Advent of Code: Day 03."""

import collections
import functools
import math
import re

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
    """Day 3: Perfectly Spherical Houses in a Vacuum."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=4),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=2),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=3),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=11),
    )

    # Convert lines to type:
    INPUT_TYPES = str

    def part1(self, parsed_input: InputType) -> int:
        pos = 0
        visited = {pos}
        for char in parsed_input[0]:
            pos += MAPPING[char]
            visited.add(pos)
        return len(visited)

    def part2(self, parsed_input: InputType) -> int:
        pos = {True: 0, False: 0}
        robot = False
        visited = {pos[robot]}
        for char in parsed_input[0]:
            pos[robot] += MAPPING[char]
            visited.add(pos[robot])
            robot = not robot
        return len(visited)


if __name__ == "__main__":
    typer.run(Day03().run)

# vim:expandtab:sw=4:ts=4
