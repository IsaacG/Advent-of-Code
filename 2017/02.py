#!/bin/python
"""Advent of Code, Day 2: Corruption Checksum."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
5 1 9 5
7 5 3
2 4 6 8""",
    """\
5 9 2 8
9 4 7 3
3 8 6 5""",
]

LineType = int
InputType = list[LineType]


class Day02(aoc.Challenge):
    """Day 2: Corruption Checksum."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=18),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=9),
    ]

    INPUT_PARSER = aoc.parse_multi_int_per_line

    def part1(self, parsed_input: InputType) -> int:
        return sum(
            max(line) - min(line)
            for line in parsed_input
        )

    def part2(self, parsed_input: InputType) -> int:
        total = 0
        for line in parsed_input:
            for a, b in itertools.combinations(sorted(line, reverse=True), 2):
                if a % b == 0:
                    total += a // b
                    break
        return total

# vim:expandtab:sw=4:ts=4
