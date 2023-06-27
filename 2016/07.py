#!/bin/python
"""Advent of Code, Day 7: Internet Protocol Version 7."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = ["""\
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn""",
    "aba[bab]xyz\naba[bab]xyz",
    "aba[bab]xyz\naaa[kek]eke",
    "aba[bab]xyz\nzazbz[bzb]cdb",
    "aba[bab]xyz\nxyx[xyx]xyx",
]

LineType = int
InputType = list[LineType]


class Day07(aoc.Challenge):
    """Day 7: Internet Protocol Version 7."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=2),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=2),
        aoc.TestCase(inputs=SAMPLE[2], part=2, want=2),
        aoc.TestCase(inputs=SAMPLE[3], part=2, want=2),
        aoc.TestCase(inputs=SAMPLE[4], part=2, want=1),
    ]

    INPUT_PARSER = aoc.parse_one_str_per_line

    def repeats(self, string: str) -> bool:
        for chars in zip(*[string[i:] for i in range(4)]):
            if chars[0] == chars[1]:
                continue
            if chars[0] == chars[3] and chars[1] == chars[2]:
                return True
        return False

    def valid(self, line: str) -> bool:
        parts = re.split(r"[][]", line)
        return not any(self.repeats(i) for i in parts[1::2]) and any(self.repeats(i) for i in parts[::2])

    def valid2(self, line: str) -> bool:
        parts = re.split(r"[][]", line)
        patterns = []
        for chunk in parts[1::2]:
            for chars in zip(*[chunk[i:] for i in range(3)]):
                if chars[0] == chars[2] != chars[1]:
                    patterns.append(chars[1] + chars[0] + chars[1])
        return any(pattern in chunk for chunk in parts[::2] for pattern in patterns)

    def part1(self, parsed_input: InputType) -> int:
        return sum(self.valid(line) for line in parsed_input)

    def part2(self, parsed_input: InputType) -> int:
        return sum(self.valid2(line) for line in parsed_input)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().input_parser(puzzle_input)
