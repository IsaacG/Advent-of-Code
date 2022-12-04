#!/bin/python
"""Advent of Code: Day 04."""

import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = ["""\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""","""\
.234.....  2-4
.....678.  6-8

.23......  2-3
...45....  4-5

....567..  5-7
......789  7-9

.2345678.  2-8
..34567..  3-7

.....6...  6-6
...456...  4-6

.23456...  2-6
...45678.  4-8
"""]
InputType = list[int]


class Day04(aoc.Challenge):
    """Day 4: Camp Cleanup."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=2),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=4),
    )

    # Convert lines to type:
    INPUT_TYPES = int
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        count = 0
        for (a1, a2), (b1, b2) in parsed_input:
            if a1 >= b1 and a2 <= b2:
                count += 1
            elif b1 >= a1 and b2 <= a2:
                count += 1
        return count

    def part2(self, parsed_input: InputType) -> int:
        count = 0
        for (a1, a2), (b1, b2) in parsed_input:
            if b1 <= a1 <= b2 or a1 <= b1 <= a2:
                count += 1
        return count

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        out = []
        for line in puzzle_input.splitlines():
            a, b = line.split(",")
            a = (int(i) for i in a.split("-"))
            b = (int(i) for i in b.split("-"))
            out.append((a, b))
        return out
        return super().parse_input(puzzle_input)

        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]

        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]


if __name__ == "__main__":
    typer.run(Day04().run)

# vim:expandtab:sw=4:ts=4
