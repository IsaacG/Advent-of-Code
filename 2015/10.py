#!/bin/python
"""Advent of Code: Day 10."""

import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = ["5 1"]

LineType = list[str]
InputType = list[LineType]


class Day10(aoc.Challenge):
    """Day 10: Elves Look, Elves Say."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=6),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=6),
    ]

    # Convert lines to type:
    INPUT_TYPES = LineType
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        if len(parsed_input) == 2:
            steps, start = parsed_input
        else:
            steps, start = 40, parsed_input[0]
        inp = list(str(start))

        for _ in range(int(steps)):
            out = []
            count = 0
            prior = inp[0]
            for char in inp:
                if char == prior:
                    count += 1
                else:
                    out.extend((str(count), prior))
                    prior = char
                    count = 1
            out.extend((str(count), prior))
            inp = out
        return len(inp)

    def part2(self, parsed_input: InputType) -> int:
        if len(parsed_input) == 2:
            steps, start = parsed_input
        else:
            steps, start = 50, parsed_input[0]
        inp = list(str(start))

        for _ in range(int(steps)):
            out = []
            count = 0
            prior = inp[0]
            for char in inp:
                if char == prior:
                    count += 1
                else:
                    out.extend((str(count), prior))
                    prior = char
                    count = 1
            out.extend((str(count), prior))
            inp = out
        return len(inp)



    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return puzzle_input.split()


if __name__ == "__main__":
    typer.run(Day10().run)

# vim:expandtab:sw=4:ts=4
