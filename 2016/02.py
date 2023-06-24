#!/bin/python
"""Advent of Code, Day 2: Bathroom Security."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = """\
ULL
RRDDD
LURDL
UUUUD"""

LineType = str
InputType = list[LineType]


class Day02(aoc.Challenge):
    """Day 2: Bathroom Security."""

    DEBUG = True
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=1985),
        aoc.TestCase(inputs=SAMPLE, part=2, want="5DB3"),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_one_str_per_line

    def part1(self, parsed_input: InputType) -> int:
        x, y = 1, 1
        out = 0
        for line in parsed_input:
            for val in line:
                match val:
                    case "U":
                        y = max(0, y - 1)
                    case "D":
                        y = min(2, y + 1)
                    case "L":
                        x = max(0, x - 1)
                    case "R":
                        x = min(2, x + 1)
            out = out * 10 + (x + y * 3 + 1)
        return out


    def part2(self, parsed_input: InputType) -> int:
        size = 5
        pad = [i.center(size) for i in ["1", "234", "56789", "ABC", "D"]]
        x, y = 0, 2
        out = []
        for line in parsed_input:
            for val in line:
                match val:
                    case "U":
                        if y > 0 and pad[y - 1][x] != " ":
                            y -= 1
                    case "D":
                        if y < size - 1 and pad[y + 1][x] != " ":
                            y += 1
                    case "L":
                        if x > 0 and pad[y][x - 1] != " ":
                            x -= 1
                    case "R":
                        if x < size - 1 and pad[y][x + 1] != " ":
                            x += 1
            out.append(pad[y][x])
        return "".join(out)

# vim:expandtab:sw=4:ts=4
