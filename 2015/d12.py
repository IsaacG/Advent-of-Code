#!/bin/python
"""Advent of Code: Day 12."""

import json

from lib import aoc

SAMPLE = [
    "[1,2,3]",
    '[1, {"a": "red", "b": 2}, 3]',
]

InputType = object


class Day12(aoc.Challenge):
    """Day 12: JSAbacusFramework.io. Count int values in JSON."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=6),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=6),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=6),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=4),
    ]

    def doc_sum(self, obj, skip_red: bool) -> int:
        """Sum integers in an object."""
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
        """Return sum ints."""
        return self.doc_sum(parsed_input, False)

    def part2(self, parsed_input: InputType) -> int:
        """Return sum ints, excluding red objects."""
        val = self.doc_sum(parsed_input, True)
        assert val < 191164
        return val

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return json.loads(puzzle_input)
