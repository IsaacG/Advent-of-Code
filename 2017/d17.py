#!/bin/python
"""Advent of Code, Day 17: Spinlock."""
from lib import aoc


class Day17(aoc.Challenge):
    """Day 17: Spinlock."""

    TESTS = [
        aoc.TestCase(part=1, inputs="3", want=638),
        aoc.TestCase(part=2, inputs="3", want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_one_int

    def part1(self, puzzle_input: int) -> int:
        """Step and insert 2017 times then return the next value."""
        step = puzzle_input
        data = [0]
        pos = 0
        for i in range(1, 2017 + 1):
            pos = (pos + step) % i + 1
            data.insert(pos % (i + 1), i)

        return data[(pos + 1) % len(data)]

    def part2(self, puzzle_input: int) -> int:
        """Return the value after 0 after 50M step-inserts."""
        step = puzzle_input
        pos = 0
        last_insert = 0
        for i in range(1, 50000000 + 1):
            pos = ((pos + step) % i) + 1
            if pos == 1:
                last_insert = i

        return last_insert

# vim:expandtab:sw=4:ts=4
