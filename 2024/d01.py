#!/bin/python
"""Advent of Code, Day 1: Historian Hysteria."""

import collections
from lib import aoc

SAMPLE = """\
3   4
4   3
2   5
1   3
3   9
3   3"""


class Day01(aoc.Challenge):
    """Day 1: Historian Hysteria."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=11),
        aoc.TestCase(part=2, inputs=SAMPLE, want=31),
    ]

    def part1(self, puzzle_input: list[list[int]]) -> int:
        """Return the sum of differences between the sorted lists."""
        a = sorted(l[0] for l in puzzle_input)
        b = sorted(l[1] for l in puzzle_input)
        return sum(abs(i - j) for i, j in zip(a, b))

    def part2(self, puzzle_input: list[list[int]]) -> int:
        """Return the sum of items times counts."""
        a = [l[0] for l in puzzle_input]
        b = collections.Counter(l[1] for l in puzzle_input)
        return sum(i * b[i] for i in a)

# vim:expandtab:sw=4:ts=4
