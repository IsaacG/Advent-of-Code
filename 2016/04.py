#!/bin/python
"""Advent of Code, Day 4: Security Through Obscurity."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re
import string

from lib import aoc

SAMPLE = [
    """\
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]"""
]

LineType = int
InputType = list[LineType]


class Day04(aoc.Challenge):
    """Day 4: Security Through Obscurity."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=1514),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_re_group_mixed(r"([\w-]+)-(\d+)\[(\w+)\]")

    def is_real(self, name: str, checksum: str) -> bool:
        name = name.replace("-", "")
        top = sorted((-v, k) for k, v in collections.Counter(name).items())
        return "".join(b for a, b in top[:5]) == checksum

    def part1(self, parsed_input: InputType) -> int:
        total = 0
        for name, sector, checksum in parsed_input:
            name = name.replace("-", "")
            top = sorted((-v, k) for k, v in collections.Counter(name).items())
            check = "".join(b for a, b in top[:5])
            if check == checksum:
                total += sector
        return total

    def part2(self, parsed_input: InputType) -> int:
        for name, sector, checksum in parsed_input:
            if not self.is_real(name, checksum):
                continue
            name = "".join(
                i if not i.isalpha() else string.ascii_lowercase[
                    (string.ascii_lowercase.index(i) + sector) % 26
                ]
                for i in name
            )
            if "northpole" in name.split("-"):
                return sector
