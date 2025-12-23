#!/bin/python
"""Advent of Code: Day 05. Map where geothermal vent clouds cross paths."""

import collections
import itertools
import re

from lib import aoc


def solve(data: list[tuple[int, int, int, int]], part: int) -> int:
    """Find hot areas where lines overlap."""
    if part == 1:
        # Filter for horizontal/vertical and call part 2.
        data = [
            (start_x, start_y, end_x, end_y)
            for start_x, start_y, end_x, end_y in data
            if start_x == end_x or start_y == end_y
        ]

    # Count points that are on lines.
    count = collections.Counter(
        itertools.chain.from_iterable(
            aoc.points_along_line(start_x, start_y, end_x, end_y)
            for start_x, start_y, end_x, end_y in data
        )
    )
    return sum(1 for v in count.values() if v > 1)


def input_parser(data: str) -> list[tuple[int, int, int, int]]:
    """Parse the input data.

    Split into lines. Split each line into a `start -> end`.
    Make a tuple(begin, end) Points for each line.
    """
    pattern = re.compile(r'^([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)$')
    lines = []
    for line in data.splitlines():
        match = pattern.match(line)
        assert match is not None
        lines.append(
            (
                int(match.group(1)), int(match.group(2)),
                int(match.group(3)), int(match.group(4)),
            )
        )
    return lines


SAMPLE = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""
TESTS = [(1, SAMPLE, 5), (2, SAMPLE, 12)]
