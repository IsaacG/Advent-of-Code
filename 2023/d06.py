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

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=288),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=71503),
    ]

    def solver(self, puzzle_input: InputType, part_one: bool) -> int:
        """Compute how long to charge the car in order to win the race."""
        if part_one:
            times, distances = ([int(i) for i in line[1:]] for line in puzzle_input)
        else:
            times, distances = ([int("".join(line[1:]))] for line in puzzle_input)

        # See notes for explanation.
        result = 1
        for time, distance in zip(times, distances):
            common = math.sqrt(time**2 - 4 * distance) / 2
            x1_exact = time / 2 - common
            x2_exact = time / 2 + common
            x1 = math.ceil(x1_exact)
            x2 = math.floor(x2_exact)
            if x1 == x1_exact:
                x1 += 1
            if x2 == x2_exact:
                x2 -= 1
            result *= (x2 - x1 + 1)
        return result

# vim:expandtab:sw=4:ts=4
