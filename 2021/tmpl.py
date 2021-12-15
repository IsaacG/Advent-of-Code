#!/bin/python
"""Advent of Code: Day ${day}."""

import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = ${sample}
InputType = list[int]


class Day${day}(aoc.Challenge):

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=0),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=0),
    )

    # Convert lines to type:
    INPUT_TYPES = int
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        return 0

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().parse_input(puzzle_input)

        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]

        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]


if __name__ == "__main__":
    typer.run(Day${day}().run)

# vim:expandtab:sw=4:ts=4
