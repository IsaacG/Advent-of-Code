#!/bin/python
"""Advent of Code, Day 16: Aunt Sue. Find the aunt who matches the criteria."""

import operator
from typing import Callable

from lib import aoc

InputType = list[dict[str, int]]
WANT_NUM = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}
OPS = {k: operator.eq for k in WANT_NUM}


class Day16(aoc.Challenge):
    """Day 16: Aunt Sue."""

    TESTS = [
        aoc.TestCase(inputs="", part=1, want=aoc.TEST_SKIP),
        aoc.TestCase(inputs="", part=2, want=aoc.TEST_SKIP),
    ]

    @staticmethod
    def matches(ops: dict[str, Callable], aunts: list[dict[str, int]]) -> int:
        """Return the aunt who matches the comparisons."""
        for i, aunt in enumerate(aunts, start=1):
            if all(ops[k](v, WANT_NUM[k]) for k, v in aunt.items()):
                return i
        raise RuntimeError("Not found.")

    def part1(self, puzzle_input: InputType) -> int:
        """Find the aunt who matches exactly."""
        return self.matches(OPS, puzzle_input)

    def part2(self, puzzle_input: InputType) -> int:
        """Find the aunt who matches more fuzzy rules."""
        ops = OPS | {
            "cats": operator.gt,
            "trees": operator.gt,
            "goldfish": operator.lt,
            "pomeranians": operator.lt,
        }
        return self.matches(ops, puzzle_input)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [
            dict(
                (prop.split(": ")[0], int(prop.split(": ")[1]))
                for prop in line.split(": ", 1)[1].split(", ")
            )
            for line in puzzle_input.splitlines()
        ]
