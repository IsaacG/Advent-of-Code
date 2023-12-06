#!/bin/python
"""Advent of Code, Day 6: Wait For It."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
Time:      7  15   30
Distance:  9  40  200""",  # 0
]

LineType = int
InputType = list[LineType]


class Day06(aoc.Challenge):
    """Day 6: Wait For It."""

    PARAMETERIZED_INPUTS = [False, True]
    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=288),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=71503),
    ]
    INPUT_PARSER = aoc.parse_ints

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        times, distances = parsed_input

        if param:
            times = [int("".join(str(i) for i in times))]
            distances = [int("".join(str(i) for i in distances))]

        return math.prod(
            sum(
                (time - i) * i > distance
                for i in range(time + 1)
            )
            for time, distance in zip(times, distances)
        )

# vim:expandtab:sw=4:ts=4
