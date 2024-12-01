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
        lists = (sorted(l) for l in zip(*puzzle_input))
        return sum(abs(i - j) for i, j in zip(*lists))

    def part2(self, puzzle_input: list[list[int]]) -> int:
        """Return the sum of items times counts."""
        a, b = zip(*puzzle_input)
        counts = collections.Counter(b)
        return sum(i * counts[i] for i in a)

# vim:expandtab:sw=4:ts=4
