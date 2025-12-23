#!/bin/python
"""Advent of Code, Day 25: Code Chronicle."""

import itertools
from lib import aoc


def solve(data: list[aoc.Map], part: int) -> int:
    """Count how many keys (loosely) fit inside a locks."""
    del part
    return sum(
        a.coords["#"].isdisjoint(b.coords["#"])
        for a, b in itertools.combinations(data, r=2)
    )


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
TESTS = [(1, SAMPLE, 3)]
# vim:expandtab:sw=4:ts=4
