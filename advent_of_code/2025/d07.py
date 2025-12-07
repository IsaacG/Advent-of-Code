#!/bin/python
"""Advent of Code, Day 7: Laboratories."""

import functools
from lib import aoc

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


class Day07(aoc.Challenge):
    """Day 7: Laboratories."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=21),
        aoc.TestCase(part=2, inputs=SAMPLE, want=40),
    ]

    def solver(self, puzzle_input: aoc.Map, part_one: bool) -> int:
        """Return how many beams get split or how many paths are taken."""
        start = puzzle_input.coords["S"].pop()
        splitters = puzzle_input.coords["^"]
        splitters_used = set[tuple[int, int]]()

        @functools.cache
        def timelines(x: int, y: int) -> int:
            """Return the number of timelines from a given point."""
            if y == puzzle_input.height:
                return 1
            y += 1
            if (x, y) in splitters:
                splitters_used.add((x, y))
                return timelines(x - 1, y) + timelines(x + 1, y)
            return timelines(x, y)

        num_timelines = timelines(*start)
        return len(splitters_used) if part_one else num_timelines

# vim:expandtab:sw=4:ts=4
