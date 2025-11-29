#!/bin/python
"""Advent of Code, Day 1: Historian Hysteria."""

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

    def solver(self, puzzle_input: list[list[int]], part_one: bool) -> int:
        """Return the similarity between two lists."""
        a, b = (sorted(line) for line in zip(*puzzle_input))
        if part_one:
            return sum(abs(i - j) for i, j in zip(a, b))
        return sum(i * b.count(i) for i in a)

# vim:expandtab:sw=4:ts=4
