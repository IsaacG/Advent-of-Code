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
        """Return if a report is safe."""
        return all(
            0 < abs(a - b) <= 3
            for a, b in zip(line, line[1:])
        ) and all(
            (a < b) == (line[0] < line[1])
            for a, b in zip(line, line[1:])
        )

    def solver(self, puzzle_input: list[list[int]], part_one: bool) -> int:
        """Return the number of safe reports, possibly allowing one reading to be removed."""
        return sum(
            (
                self.safe(line)
                or any(
                    self.safe(line[:i] + line[i + 1:])
                    for i in range(0 if part_one else len(line))
                )
            )
            for line in puzzle_input
        )

# vim:expandtab:sw=4:ts=4
