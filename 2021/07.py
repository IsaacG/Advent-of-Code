#!/bin/python
"""Advent of Code: Day 07."""

import collections
import functools
import math
import re
from typing import Any, Callable

import typer

from lib import aoc

InputType = list[int]

SAMPLE = ["""\
16,1,2,0,4,2,7,1,2,14
"""]

class Day07(aoc.Challenge):

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=37),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=168),
    )

    # Convert lines to type:
    INPUT_TYPES = int
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, lines: InputType) -> int:
        costs = []
        for i in range(min(lines), max(lines) + 1):
            costs.append(sum(abs(i - l) for l in lines))
        return min(costs)
          
    def part2(self, lines: InputType) -> int:

        def s(n):
            return n*(n+1)//2

        costs = []
        for i in range(min(lines), max(lines) + 1):
            costs.append(sum(s(abs(i - l)) for l in lines))
        return min(costs)

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data. Comma separated ints."""
        return [int(i) for i in puzzle_input.split(",")]


if __name__ == "__main__":
    typer.run(Day07().run)
