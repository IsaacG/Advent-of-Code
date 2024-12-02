#!/bin/python
"""Advent of Code, Day 2: Red-Nosed Reports."""

from lib import aoc

SAMPLE = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""


class Day02(aoc.Challenge):
    """Day 2: Red-Nosed Reports."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=2),
        aoc.TestCase(part=2, inputs=SAMPLE, want=4),
    ]

    def safe(self, line: list[int]) -> bool:
        """Return if a report is safe.

        A report is safe if the values are monotonically increasing/decreasing
        and with a step always between 1 and 3.
        """
        sign = aoc.sign(line[1] - line[0])
        return all(
                aoc.sign(b - a) == sign
                and 1 <= abs(b - a) <= 3
            for a, b in zip(line, line[1:])
        )

    def part1(self, puzzle_input: list[list[int]]) -> int:
        """Return the number of safe reports."""
        return sum(self.safe(line) for line in puzzle_input)

    def part2(self, puzzle_input: list[list[int]]) -> int:
        """Return the number of safe reports, allowing one reading to be ignored."""
        return sum(
            any(
                self.safe(line[:i] + line[i + 1:])
                for i in range(len(line))
            )
            for line in puzzle_input
        )

# vim:expandtab:sw=4:ts=4
