#!/bin/python
"""Advent of Code, Day 2: Corruption Checksum."""
from __future__ import annotations

import itertools

from lib import aoc

SAMPLE = [
    """\
5 1 9 5
7 5 3
2 4 6 8""",
    """\
5 9 2 8
9 4 7 3
3 8 6 5""",
]


class Day02(aoc.Challenge):
    """Day 2: Corruption Checksum. Compute checksums of lines."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=18),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=9),
    ]
    INPUT_PARSER = aoc.parse_multi_int_per_line

    def part1(self, puzzle_input: list[list[int]]) -> int:
        """Return the sum difference between the largest and smallest value on each line."""
        return sum(
            max(line) - min(line)
            for line in puzzle_input
        )

    def part2(self, puzzle_input: list[list[int]]) -> int:
        """Return the sum quotient between two evenly divisible numbers on each line."""
        return sum(
            next(
                a // b
                for a, b in itertools.combinations(sorted(line, reverse=True), 2)
                if a % b == 0
            )
            for line in puzzle_input
        )

# vim:expandtab:sw=4:ts=4
