#!/bin/python
"""Advent of Code, Day 25: Code Chronicle."""

import itertools
from lib import aoc

SAMPLE = """\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""


class Day25(aoc.Challenge):
    """Day 25: Code Chronicle."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=3),
        aoc.TestCase(part=2, inputs=SAMPLE, want=aoc.TEST_SKIP),
    ]

    def part1(self, puzzle_input: list[aoc.Map]) -> int:
        """Count how many keys (loosely) fit inside a locks."""
        return sum(
            a.coords["#"].isdisjoint(b.coords["#"])
            for a, b in itertools.combinations(puzzle_input, r=2)
        )

# vim:expandtab:sw=4:ts=4
