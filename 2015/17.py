#!/bin/python
"""Advent of Code, Day 17: No Such Thing as Too Much."""

import collections
import itertools
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = ["""\
20
15
10
5
5"""
]

LineType = int
InputType = list[LineType]


class Day17(aoc.Challenge):
    """Day 17: No Such Thing as Too Much."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=4),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=3),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    # Convert lines to type:
    INPUT_TYPES = LineType
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        target = 25 if self.testing else 150
        count = 0
        for n in range(len(parsed_input)):
            for combo in itertools.combinations(parsed_input, n):
                if sum(combo) == target:
                    count += 1
        return count

    def part2(self, parsed_input: InputType) -> int:
        target = 25 if self.testing else 150
        count = collections.defaultdict(int)
        for n in range(len(parsed_input)):
            for combo in itertools.combinations(parsed_input, n):
                if sum(combo) == target:
                    count[n] += 1
        return count[min(count)]

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().input_parser(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]
        # Words: mixed str and int
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in line.split()
            )
            for line in puzzle_input.splitlines()
        ]
        # Regex splitting
        patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in patt.match(line).groups()
            )
            for line in puzzle_input.splitlines()
        ]

    # def line_parser(self, line: str):
    #     pass


if __name__ == "__main__":
    typer.run(Day17().run)

# vim:expandtab:sw=4:ts=4
