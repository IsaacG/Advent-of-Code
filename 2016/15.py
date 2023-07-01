#!/bin/python
"""Advent of Code, Day 15: Timing is Everything."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = """\
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1."""

LineType = int
InputType = list[LineType]


class Day15(aoc.Challenge):
    """Day 15: Timing is Everything."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=5),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        print(parsed_input)
        disks = [
            (number + start, positions)
            for number, positions, _, start in parsed_input
        ]
        print(disks)
        for time in itertools.count():
            if all(
                ((start + time) % positions) == 0
                for start, positions in disks
            ):
                return time

    def part2(self, parsed_input: InputType) -> int:
        last = len(parsed_input)
        got = self.part1(parsed_input + [[last + 1, 11, 0, 0]])
        assert got < 3730820
        return got
