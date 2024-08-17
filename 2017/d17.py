#!/bin/python
"""Advent of Code, Day 17: Spinlock."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = ["3"
]

LineType = int
InputType = list[LineType]


class Day17(aoc.Challenge):
    """Day 17: Spinlock."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=638),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_one_int

    def part1(self, parsed_input: InputType) -> int:
        step = parsed_input
        data = [0]
        pos = 0
        for i in range(1, 2017 + 1):
            pos = (pos + step) % i + 1
            data.insert((pos + 1) % (i + 1), i)
            pos += 1

        return data[(pos + 1) % 2018]

    def part2(self, parsed_input: InputType) -> int:
        step = parsed_input
        data = [0]
        pos = 0
        last_insert = 0
        for i in range(1, 50000000 + 1):
            pos = ((pos + step) % i) + 1
            if pos == 1:
                last_insert = i

        return last_insert

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

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


# vim:expandtab:sw=4:ts=4
