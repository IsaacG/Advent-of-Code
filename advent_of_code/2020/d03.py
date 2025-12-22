#!/usr/bin/env python
"""AoC Day 3: Toboggan Trajectory."""
import math
from lib import aoc


def tree_count(grid, x_step, y_step) -> int:
    """Count tree encounters for a given path."""
    count = 0
    x = 0
    for y in range(0, grid.height, y_step):
        if grid.chars[x % grid.width, y] == '#':
            count += 1
        x += x_step
    return count


def solve(data: aoc.Map, part: int) -> int:
    """Return tree encounters."""
    if part == 1:
        return tree_count(data, 3, 1)

    return math.prod(
        tree_count(data, x_step, y_step)
        for x_step, y_step in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    )


SAMPLE = """\
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
"""
TESTS = [(1, SAMPLE, 7), (2, SAMPLE, 336)]
