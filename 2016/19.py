#!/bin/python
"""Advent of Code, Day 19: An Elephant Named Joseph."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = "5"

InputType = int


class Day19(aoc.Challenge):
    """Day 19: An Elephant Named Joseph."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=3),
        aoc.TestCase(inputs=SAMPLE, part=2, want=2),
    ]

    def part1(self, parsed_input: InputType) -> int:
        circle = list(range(parsed_input))
        while len(circle) > 1:
            odd = len(circle) % 2
            circle = circle[::2]
            if odd:
                circle = circle[1:]
        got = circle[0] + 1
        if not self.testing:
            assert got > 917453, got
        return got

    def part2(self, parsed_input: InputType) -> int:
        stop = parsed_input - 1
        size = 1
        while True:
            counter = 1
            while counter <= size // 2:
                if size == stop:
                    return counter
                size += 1
                counter += 1
            while counter <= size + 1:
                if size == stop:
                    return counter
                size += 1
                counter += 2
