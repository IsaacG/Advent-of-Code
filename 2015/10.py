#!/bin/python
"""Advent of Code: Day 10."""

import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = "1"

LineType = list[str]
InputType = list[LineType]


def look_say(string: str) -> str:
    str_len = len(string)
    out = []
    count = 0
    prior = string[0]
    for char in string:
        if char == prior:
            count += 1
        else:
            out.extend((str(count), prior))
            prior = char
            count = 1
    out.extend((str(count), prior))
    return "".join(out)


class Day10(aoc.Challenge):
    """Day 10: Elves Look, Elves Say."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=6),
        aoc.TestCase(inputs=SAMPLE, part=2, want=6),
    ]

    # Convert lines to type:
    INPUT_TYPES = LineType
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def look_say_loop(self, string: str, steps: int) -> str:
        for _ in range(5 if self.testing else steps):
            string = look_say(string)
        return string

    def part1(self, parsed_input: InputType) -> int:
        return len(self.look_say_loop(parsed_input, 40))

    def part2(self, parsed_input: InputType) -> int:
        return len(self.look_say_loop(parsed_input, 50))

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return puzzle_input


if __name__ == "__main__":
    typer.run(Day10().run)

# vim:expandtab:sw=4:ts=4
