#!/bin/python
"""Advent of Code, Day 18: Like a Rogue."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = ".^^.^.^^^^"

InputType = str


class Day18(aoc.Challenge):
    """Day 18: Like a Rogue."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=38),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        width, traps = parsed_input
        rows = 10 if self.testing else 40
        safe = 0
        for _ in range(rows):
            safe += width - len(traps)
            traps = {
                col
                for col in range(width)
                if (col - 1 in traps) != (col + 1 in traps)
            }

        return safe

    def part2(self, parsed_input: InputType) -> int:
        width, traps = parsed_input
        rows = 400000
        safe = 0
        for _ in range(rows):
            safe += width - len(traps)
            traps = {
                col
                for col in range(width)
                if (col - 1 in traps) != (col + 1 in traps)
            }

        return safe

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return len(puzzle_input), {i for i, char in enumerate(puzzle_input) if char == "^"}
