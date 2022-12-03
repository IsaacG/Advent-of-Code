#!/bin/python
"""Advent of Code: Day 02."""

import collections
import itertools
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = ["2x3x4", "1x1x10"]
InputType = list[list[int]]


class Day02(aoc.Challenge):
    """Day 2: I Was Told There Would Be No Math."""

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=58),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=43),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=34),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=14),
    )

    def part1(self, parsed_input: InputType) -> int:
        total = 0
        for dims in parsed_input:
            sides = [a * b for a, b in itertools.combinations(dims, 2)]
            total += sum(sides) * 2 + min(sides)
        return total

    def part2(self, parsed_input: InputType) -> int:
        total = 0
        for dims in parsed_input:
            perimeters = [a + b for a, b in itertools.combinations(dims, 2)]
            total += min(perimeters) * 2 + self.mult(dims)
        return total

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [[int(i) for i in line.split("x")] for line in puzzle_input.splitlines()]


if __name__ == "__main__":
    typer.run(Day02().run)

# vim:expandtab:sw=4:ts=4
