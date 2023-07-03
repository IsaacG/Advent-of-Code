#!/bin/python
"""Advent of Code, Day 20: Firewall Rules."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = """\
5-8
0-2
4-7"""

LineType = int
InputType = list[LineType]


class Day20(aoc.Challenge):
    """Day 20: Firewall Rules."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=3),
        aoc.TestCase(inputs=SAMPLE, part=2, want=2),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        cur = 0
        for low, high in parsed_input:
            if low <= cur and cur <= high:
                cur = high + 1
            elif cur < low:
                return cur

    def part2(self, parsed_input: InputType) -> int:
        if self.testing:
            parsed_input.append((10, 10))
        else:
            parsed_input.append((4294967296, 4294967296))
        cur = 0
        allowed = 0
        for low, high in parsed_input:
            if low <= cur and cur <= high:
                cur = high + 1
            elif cur < low:
                allowed += low - cur
                cur = high + 1
        return allowed

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return sorted(tuple(int(i) for i in line.split("-")) for line in puzzle_input.splitlines())
