#!/bin/python
"""Advent of Code: Day 12."""

import collections
import functools
import json
import math
import re

import typer
from lib import aoc

SAMPLE = [
    "[1,2,3]",
    '[1, {"a": "red", "b": 2}, 3]',
]

LineType = int
InputType = list[LineType]


class Day12(aoc.Challenge):
    """Day 12: JSAbacusFramework.io."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=6),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=6),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=6),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=4),
    ]

    # Convert lines to type:
    INPUT_TYPES = LineType
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def doc_sum(self, obj, skip_red: bool) -> int:
        if isinstance(obj, str):
            return 0
        if isinstance(obj, int):
            return obj
        if isinstance(obj, list):
            return sum(self.doc_sum(i, skip_red) for i in obj)
        if isinstance(obj, dict):
            if skip_red and "red" in obj.values():
                return 0
            return sum(self.doc_sum(i, skip_red) for i in obj.values())
        raise ValueError(obj)

    def part1(self, parsed_input: InputType) -> int:
        return self.doc_sum(parsed_input, False)

    def part2(self, parsed_input: InputType) -> int:
        val = self.doc_sum(parsed_input, True)
        assert val < 191164
        return val

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return json.loads(puzzle_input)


if __name__ == "__main__":
    typer.run(Day12().run)

# vim:expandtab:sw=4:ts=4
