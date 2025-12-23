#!/bin/python
"""Advent of Code: Day 01."""

from lib import aoc

SAMPLE = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""


class Day01(aoc.Challenge):
    """Day 1: Calorie Counting. Count how many calories the elves have."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=24000),
        aoc.TestCase(inputs=SAMPLE, part=2, want=45000),
    ]

    def part1(self, puzzle_input: list[list[int]]) -> int:
        """Return the sum calories held by the elf with the most calories."""
        return max(sum(i) for i in puzzle_input)

    def part2(self, puzzle_input: list[list[int]], top_n: int = 3) -> int:
        """Return the sum calories held by the top three elves with the most calories."""
        return sum(sorted(sum(i) for i in puzzle_input)[-top_n:])
