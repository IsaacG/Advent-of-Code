#!/bin/python
"""Advent of Code, Day 7: Laboratories."""

import functools
from lib import aoc


def solve(data: aoc.Map, part: int) -> int:
    """Return how many beams get split or how many paths are taken."""
    start = data.coords["S"].pop()
    splitters = data.coords["^"]
    splitters_used = set[tuple[int, int]]()

    @functools.cache
    def timelines(x: int, y: int) -> int:
        """Return the number of timelines from a given point."""
        if y == data.height:
            return 1
        y += 1
        if (x, y) in splitters:
            splitters_used.add((x, y))
            return timelines(x - 1, y) + timelines(x + 1, y)
        return timelines(x, y)

    num_timelines = timelines(*start)
    return len(splitters_used) if part == 1 else num_timelines


SAMPLE = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
TESTS = [(1, SAMPLE, 21), (2, SAMPLE, 40)]
# vim:expandtab:sw=4:ts=4
