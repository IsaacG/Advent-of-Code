#!/bin/python
"""Advent of Code: Day 01."""

import collections
import functools
import math
import re
from typing import Generator

import typer
from lib import aoc

SAMPLE = ["(())", "()()", "(()(()(", ")", "()())"]
InputType = list[int]
MAPPING = {"(": 1, ")": -1}


class Day01(aoc.Challenge):

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=0),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=0),
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=3),
        aoc.TestCase(inputs=SAMPLE[3], part=2, want=1),
        aoc.TestCase(inputs=SAMPLE[4], part=2, want=5),
    )

    # Convert lines to type:
    INPUT_TYPES = str
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        return sum(MAPPING[i] for i in parsed_input[0])

    def part2(self, parsed_input: InputType) -> int:

        def gen(line: str) -> Generator[str, tuple[int, int], None]:
            floor = 0
            for count, i in enumerate(line, start=1):
                floor += MAPPING[i]
                yield count, floor

        return next(count for count, floor in gen(parsed_input[0]) if floor == -1)

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().parse_input(puzzle_input)

        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]

        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]


if __name__ == "__main__":
    typer.run(Day01().run)

# vim:expandtab:sw=4:ts=4
