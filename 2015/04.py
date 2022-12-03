#!/bin/python
"""Advent of Code: Day 04."""

import collections
import hashlib
import math
import re

import typer
from lib import aoc

SAMPLE = ["abcdef", "pqrstuv"]
InputType = list[int]


class Day04(aoc.Challenge):
    """Day 4: The Ideal Stocking Stuffer."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=609043),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=1048970),
    )

    # Convert lines to type:
    INPUT_TYPES = str
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        key = parsed_input[0]
        for i in range(0, 1000000):
            data = key + str(i)
            if hashlib.md5(data.encode()).hexdigest().startswith("00000"):
                return i

    def part2(self, parsed_input: InputType) -> int:
        key = parsed_input[0]
        for i in range(0, 100000000):
            data = key + str(i)
            if hashlib.md5(data.encode()).hexdigest().startswith("000000"):
                return i

if __name__ == "__main__":
    typer.run(Day04().run)

# vim:expandtab:sw=4:ts=4
