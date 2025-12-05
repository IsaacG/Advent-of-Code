#!/bin/python
"""Advent of Code, Day 5: Cafeteria."""
from lib import aoc

SAMPLE = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32"""


class Day05(aoc.Challenge):
    """Day 5: Cafeteria."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=3),
        aoc.TestCase(part=2, inputs=SAMPLE, want=14),
    ]

    def part1(self, puzzle_input: list[list[int] | list[list[int]]]) -> int:
        """Return how many available ingredients are fresh."""
        fresh, available = puzzle_input
        return sum(
            any(x <= ingredient <= y for x, y in fresh)
            for ingredient in available
        )

    def part2(self, puzzle_input: list[list[list[int]]]) -> int:
        """Return how many fresh ingredients exist."""
        fresh, _ = puzzle_input
        fresh.sort()

        opened, closed = fresh[0]
        total = 0
        for start, end in fresh[1:]:
            if start > closed:
                total += 1 + closed - opened
                opened, closed = start, end
            else:
                closed = max(closed, end)
        total += 1 + closed - opened
        return total

# vim:expandtab:sw=4:ts=4
