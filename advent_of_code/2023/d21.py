#!/bin/python
"""Advent of Code, Day 21: Step Counter."""
from lib import aoc


def walk(start: set[tuple[int, int]], garden: set[tuple[int, int]], steps: int) -> int:
    """Return reachable coordinates after walking N steps from the start."""
    for _ in range(steps):
        new = set[tuple[int, int]]()
        # Expand all coordinates to their neighbors.
        for coord in start:
            new.update(aoc.t_neighbors4(coord))
        # Restrict to valid locations.
        start = new & garden
    return len(start)


def solve(data: aoc.Map, part: int, testing: bool) -> int:
    """Return the number of reachable locations in N steps."""
    size, start, garden = data.size, data.coords["S"], data.coords["."]
    garden.update(start)
    steps = 6 if testing else 64 if part == 1 else 26501365
    if part == 1:
        return walk(start, garden, steps)

    half_size = (size - 1) // 2
    max_x = data.max_x
    max_y = data.max_y
    center = (half_size, half_size)  # This should be the start location.

    centered_edges = [(max_x, half_size), (half_size, 0), (0, half_size), (half_size, max_y)]
    corners = [(max_x, max_y), (max_x, 0), (0, 0), (0, max_y)]

    # Start at the middle of an edge and walk to the far side.
    tips = sum(walk({start}, garden, size - 1) for start in centered_edges)
    # Start at the middle of two edges.
    large_diag = sum(
        walk({centered_edges[i], centered_edges[(i + 1) % 4]}, garden, size - 1)
        for i in range(4)
    )
    # Start at a corner.
    short_diag = sum(walk({start}, garden, half_size - 1) for start in corners)
    interior_center = walk({center}, garden, size)
    interior_even = walk({center}, garden, size - 1)

    expansions = (steps - half_size) // size
    return (
        tips
        + (expansions - 1) * large_diag
        + expansions * short_diag
        + interior_center * (expansions - 1) ** 2
        + interior_even * expansions ** 2
    )


SAMPLE = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
TESTS = [(1, SAMPLE, 16)]
# vim:expandtab:sw=4:ts=4
