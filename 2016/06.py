#!/bin/python
"""Advent of Code, Day 6: Signals and Noise."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = """\
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar"""

LineType = int
InputType = list[LineType]


class Day06(aoc.Challenge):
    """Day 6: Signals and Noise."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want="easter"),
        aoc.TestCase(inputs=SAMPLE, part=2, want="advent"),
    ]

    INPUT_PARSER = aoc.parse_one_str_per_line

    def part1(self, parsed_input: InputType) -> int:
        return "".join(collections.Counter(col).most_common(1)[0][0] for col in zip(*parsed_input))

    def part2(self, parsed_input: InputType) -> int:
        return "".join(collections.Counter(col).most_common()[-1][0] for col in zip(*parsed_input))
