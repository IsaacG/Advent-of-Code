#!/bin/python
"""Advent of Code: Day 01."""

from typing import Generator

import typer
from lib import aoc

SAMPLE = ["(())", "()()", "(()(()(", ")", "()())"]
InputType = str
MAPPING = {"(": 1, ")": -1}


class Day01(aoc.Challenge):
    """Day 1: Not Quite Lisp. Count Santa's floor level."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=0),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=0),
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=3),
        aoc.TestCase(inputs=SAMPLE[3], part=2, want=1),
        aoc.TestCase(inputs=SAMPLE[4], part=2, want=5),
    )

    INPUT_TYPES = str

    def part1(self, parsed_input: InputType) -> int:
        """Return Santa's final floor."""
        return sum(MAPPING[i] for i in parsed_input)

    def part2(self, parsed_input: InputType) -> int:
        """Return when Santa hits the basement."""
        floor = 0
        for count, i in enumerate(parsed_input, start=1):
            floor += MAPPING[i]
            if floor == -1:
                return count

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return puzzle_input


if __name__ == "__main__":
    typer.run(Day01().run)

# vim:expandtab:sw=4:ts=4
