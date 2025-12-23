#!/bin/python
"""Advent of Code: Day 09. Find low points and basins in a topographic map."""

import math
import typing
from lib import aoc


def lows(depths: dict[tuple[int, int], int]) -> list[tuple[int, int]]:
    """Return all the minimum points on the map."""
    return [
        point
        for point, depth in depths.items()
        if all(
            depth < depths.get(n, 10) for n in aoc.t_neighbors4(point)
        )
    ]


def solve(data: aoc.Map, part: int) -> int:
    """Find basins on the map."""
    depths = typing.cast(dict[tuple[int, int], int], data.chars)
    if part == 1:
        # Find all the low points on the map.
        return sum(depths[point] + 1 for point in lows(depths))

    # Find the largest three basins.
    # Simply remove 9's from the map and find the size of each island.
    # Remove borders around the islands, i.e. points of height 9.
    unexplored = {point for point, depth in data.chars.items() if depth != 9}
    basins = aoc.partition_regions(unexplored, predicate=lambda a, b: True)
    basin_sizes = (len(basin) for basin in basins)

    return math.prod(sorted(basin_sizes, reverse=True)[:3])


SAMPLE = """\
2199943210
3987894921
9856789892
8767896789
9899965678
"""
TESTS = [(1, SAMPLE, 15), (2, SAMPLE, 1134)]
