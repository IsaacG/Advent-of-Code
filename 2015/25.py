#!/bin/python
"""Advent of Code, Day 25: Let It Snow."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = ["1 1", "2 6", "6 4"]

LineType = int
InputType = list[LineType]


class Day25(aoc.Challenge):
    """Day 25: Let It Snow."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=20151125),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=4041754),
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=24659492),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=0),
    ]

    INPUT_PARSER = aoc.parse_re_findall_int(r"\d+")

    def part1(self, parsed_input: InputType) -> int:
        row, column = parsed_input[0]
        code_num = 1
        for i in range(1, row):
            code_num += i
        for i in range(row + 1, row + column):
            code_num += i
        code = 20151125
        for i in range(code_num - 1):
            code = (code * 252533) % 33554393
        return code


if __name__ == "__main__":
    typer.run(Day25().run)

# vim:expandtab:sw=4:ts=4
