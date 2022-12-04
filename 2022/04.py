#!/bin/python
"""Advent of Code: Day 04."""

import re

import typer
from lib import aoc

SAMPLE = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
InputType = tuple[int, int, int, int]


class Day04(aoc.Challenge):
    """Day 4: Camp Cleanup. Detect overlapping ranges."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=2),
        aoc.TestCase(inputs=SAMPLE, part=2, want=4),
    )

    def part1(self, parsed_input: InputType) -> int:
        """Return the number of fully contained overlaps."""
        return sum(
            True
            for a1, a2, b1, b2 in parsed_input
            if (a1 >= b1 and a2 <= b2) or (b1 >= a1 and b2 <= a2)
        )

    def part2(self, parsed_input: InputType) -> int:
        """Return the number of partial overlaps."""
        return sum(
            True
            for a1, a2, b1, b2 in parsed_input
            if b1 <= a1 <= b2 or a1 <= b1 <= a2
        )

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        patt = re.compile(r"[,-]")
        return [
            (int(i) for i in patt.split(line))
            for line in puzzle_input.splitlines()
        ]


if __name__ == "__main__":
    typer.run(Day04().run)

# vim:expandtab:sw=4:ts=4
