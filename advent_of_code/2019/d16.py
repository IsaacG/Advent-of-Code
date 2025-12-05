#!/bin/python
"""Advent of Code, Day 16: Flawed Frequency Transmission."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

BASE_PATTERN = [0, 1, 0, -1]


class Day16(aoc.Challenge):
    """Day 16: Flawed Frequency Transmission."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs="80871224585914546619083218645595", part=1, want=24176176),
        # aoc.TestCase(inputs="19617804207202209144916044189917", part=1, want=73745418),
        # aoc.TestCase(inputs="69317163492948606335995924319873", part=1, want=52432133),
        aoc.TestCase(inputs="", part=2, want=0),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_one_str

    @functools.cache
    def pattern(self, position: int) -> list[int]:
        pattern = [i for b in BASE_PATTERN for i in [b] * (position + 1)]
        return pattern

    def part1(self, puzzle_input: str) -> int:
        signal = [int(i) for i in puzzle_input]
        length = len(signal)
        for _ in range(100):
            signal = [
                abs(
                    sum(
                        a * b
                        for a, b in zip([0] + signal, itertools.cycle(self.pattern(position)))
                    )
                ) % 10
                for position in range(length)
            ]
        return int(str("".join(str(i) for i in signal[:8])))

    def part2(self, puzzle_input: str) -> int:
        raise NotImplementedError

    def solver(self, puzzle_input: str, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> str:
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
