#!/bin/python
"""Advent of Code: Day 06."""

import collections
import functools
import math
import re
from typing import Any, Callable

import typer

from lib import aoc

SAMPLE = ["""\
3,4,3,1,2
"""]

InputType = list[int]


class Day06(aoc.Challenge):

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=5934),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=26984457539),
    )

    # Convert lines to type:
    INPUT_TYPES = int
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, lines: InputType) -> int:
        fish = lines
        for i in range(80):
            new = sum(1 for i in fish if i == 0)
            fish = [i - 1 for i in fish if i] + [8] * new + [6] * new
        return len(fish)

    def part2(self, lines: InputType) -> int:
        counter = dict(collections.Counter(lines))
        for i in range(256):
            new = {k - 1: v for k, v in counter.items() if k}
            new[6] = counter.get(0, 0) + counter.get(7, 0)
            new[8] = counter.get(0, 0)
            counter = new
        return sum(v for v in counter.values())

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [int(i) for i in puzzle_input.split(",")]


if __name__ == "__main__":
    typer.run(Day06().run)
