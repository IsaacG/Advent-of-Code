#!/bin/python
"""Advent of Code, Day 11: Cosmic Expansion."""
import itertools
from lib import aoc


def solve(data: aoc.Map, part: int) -> int:
    """Return the sum of the distances between shifted galaxies."""
    stars = data.coords["#"]
    distance = 1 if part == 1 else 1_000_000 - 1
    min_x, min_y, max_x, max_y = data.edges

    # Compute the shift for each column and row.
    offset_columns = []
    offset = 0
    for x in range(min_x, max_x + 1):
        if not any(pos[0] == x for pos in stars):
            offset += distance
        offset_columns.append(offset)

    offset_rows = []
    offset = 0
    for y in range(min_y, max_y + 1):
        if not any(pos[1] == y for pos in stars):
            offset += distance
        offset_rows.append(offset)

    # Shift all galaxies.
    stars = {
        (pos[0] + offset_columns[pos[0]], pos[1] + offset_rows[pos[1]])
        for pos in stars
    }

    return int(
        sum(
            abs(b[0] - a[0]) + abs(b[1] - a[1])
            for a, b in itertools.combinations(stars, 2)
        )
    )


SAMPLE = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
TESTS = [(1, SAMPLE, 374)]
# vim:expandtab:sw=4:ts=4
