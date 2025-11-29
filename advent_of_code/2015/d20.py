#!/bin/python
"""Advent of Code, Day 20: Infinite Elves and Infinite Houses."""

from lib import aoc

SAMPLE = ["70", "130"]


class Day20(aoc.Challenge):
    """Day 20: Infinite Elves and Infinite Houses."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=4),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=8),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, puzzle_input: int) -> int:
        target = puzzle_input // 10

        limit = 1000000
        houses = [1] * limit
        for i in range(2, limit):
            for house in range(i, limit, i):
                houses[house] += i

        for i, num in enumerate(houses):
            if num >= target:
                return i

        raise RuntimeError

    def part2(self, puzzle_input: int) -> int:
        target = puzzle_input // 11

        limit = 1000000
        houses = [1] * limit
        for i in range(2, limit):
            for house in range(i, min(limit, i * 51), i):
                houses[house] += i

        for i, num in enumerate(houses):
            if num >= target:
                return i

        raise RuntimeError
