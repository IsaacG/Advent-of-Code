#!/bin/python
"""Advent of Code, Day 3: Squares With Three Sides."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    '5 10 25\n1 1 1',  # 0
]

LineType = int
InputType = list[LineType]


class Day03(aoc.Challenge):
    """Day 3: Squares With Three Sides."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=1),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_re_findall_int(r"\d+")

    def part1(self, parsed_input: InputType) -> int:
        return sum(2 * max(vals) < sum(vals) for vals in parsed_input)

    def part2(self, parsed_input: InputType) -> int:
        vals = [
            row[i:i + 3]
            for row in zip(*parsed_input)
            for i in range(0, len(row), 3)
        ]
        return self.part1(vals)
