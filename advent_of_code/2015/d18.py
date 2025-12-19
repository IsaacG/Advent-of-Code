#!/bin/python
"""Advent of Code, Day 18: Like a GIF For Your Yard. Conway's Game of Life."""
from lib import aoc


def simulate(bitmap: aoc.Map, cycles: int, corners: bool) -> int:
    """Run Conway's Game of Life and return number of lights on at end."""
    # The number of neighbors which will turn a light on.
    want = {True: (2, 3), False: (3,)}
    # Track just the lights which are on.
    on = bitmap.coords["#"]
    corner_points = bitmap.corners

    for _ in range(cycles):
        if corners:
            on.update(corner_points)
        # Consider cells which are on or adjacent to an on.
        candidates = {
            (x + dx, y + dy)
            for x, y in on
            for dx, dy in aoc.ALL_NEIGHBORS_T
            if (x + dx, y + dy) in bitmap.all_coords
        } | on

        new = set()
        for point in candidates:
            x, y = point
            count = sum((x + dx, y + dy) in on for dx, dy in aoc.ALL_NEIGHBORS_T)
            if count in want[point in on]:
                new.add(point)
        on = new

    if corners:
        on.update(corner_points)
    return len(on)


def solve(data: aoc.Map, part: int, testing: bool) -> int:
    """Return the number of lights on, with corners possibly stuck."""
    cycles = 100
    if testing:
        cycles = 4 if part == 1 else 5
    return simulate(data, cycles, part == 2)


SAMPLE = """\
.#.#.#
...##.
#....#
..#...
#.#..#
####.."""
TESTS = [(1, SAMPLE, 4), (2, SAMPLE, 17)]
