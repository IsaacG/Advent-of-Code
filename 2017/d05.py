#!/bin/python
"""Advent of Code, Day 5: A Maze of Twisty Trampolines, All Alike."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
0
3
0
1
-3""",  # 5
]

LineType = int
InputType = list[LineType]


class Day05(aoc.Challenge):
    """Day 5: A Maze of Twisty Trampolines, All Alike."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=5),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=10),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_one_int_per_line

    def part1(self, parsed_input: InputType) -> int:
        mem = parsed_input.copy()
        size = len(mem)
        ptr = 0

        step = 0
        while 0 <= ptr < size:
            offset = mem[ptr]
            mem[ptr] += 1
            ptr += offset
            step += 1
        return step

    def part2(self, parsed_input: InputType) -> int:
        mem = parsed_input.copy()
        size = len(mem)
        ptr = 0

        step = 0
        while 0 <= ptr < size:
            offset = mem[ptr]
            mem[ptr] += -1 if offset >= 3 else 1
            ptr += offset
            step += 1
        return step

# vim:expandtab:sw=4:ts=4
