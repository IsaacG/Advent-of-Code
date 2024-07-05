#!/bin/python
"""Advent of Code, Day 11: Hex Ed."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    ('ne,ne,ne', 3),
    ('ne,ne,sw,sw', 0),
    ('ne,ne,s,s', 2),
    ('se,sw,se,sw,sw', 3),
]

LineType = int
InputType = list[LineType]


class Day11(aoc.Challenge):
    """Day 11: Hex Ed."""

    PARAMETERIZED_INPUTS = [True, False]
    TESTS = [
        aoc.TestCase(part=1, inputs=data, want=want)
        for data, want in SAMPLE
    ] + [
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_one_str

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        location = complex()
        farthest = 0
        offsets = aoc.HEX_AXIAL_DIRS_FLAT_TOP

        def axial_distance() -> int:
            """Taken from https://www.redblobgames.com/grids/hexagons/#distances."""
            q, r = int(location.real), int(location.imag)
            return (abs(q) + abs(q + r) + abs(r)) // 2

        for direction in parsed_input.split(","):
            location += offsets[direction]
            farthest = max(farthest, axial_distance())
        distance = axial_distance()
        return distance if param else farthest

# vim:expandtab:sw=4:ts=4
