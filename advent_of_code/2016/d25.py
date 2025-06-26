#!/bin/python
"""Advent of Code, Day 25: Clock Signal. Find the starting value which generates a clock signal."""

import itertools
from lib import aoc
import assembunny


class Day25(aoc.Challenge):
    """Day 25: Clock Signal."""

    TESTS = [
        aoc.TestCase(inputs="", part=1, want=aoc.TEST_SKIP),
        aoc.TestCase(inputs="", part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, puzzle_input: list[str]) -> int:
        """Find the starting value which generates a clock signal."""
        computer = assembunny.Assembunny(puzzle_input)
        return next(
            i for i in itertools.count(start=0)
            if computer.run(register_a=i)[1]
        )
