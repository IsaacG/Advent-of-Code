#!/bin/python
"""Advent of Code, Day 6: Chronal Coordinates."""
from __future__ import annotations

from lib import aoc


def minmax(data: list[list[int]]) -> tuple[int, int, int, int]:
    """Return the boundaries of the puzzle."""
    min_x = min(x for x, y in data)
    max_x = max(x for x, y in data)
    min_y = min(y for x, y in data)
    max_y = max(y for x, y in data)
    return min_x, max_x, min_y, max_y


def solve(data: list[list[int]], part: int, testing: bool) -> int:
    """Return the largest contained region."""
    min_x, max_x, min_y, max_y = minmax(data)
    
    if part == 1:
        controls: dict[tuple[int, int], set[tuple[int, int]]] = {(x, y): set() for x, y in data}

        # For every location in the puzzle, compute the distances to all nodes.
        # If there is no tie, associate the location with the closest node.
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                distances = sorted((abs(x - px) + abs(y - py), (px, py)) for px, py in data)[:2]
                if distances[0][0] != distances[1][0]:
                    controls[distances[0][1]].add((x, y))
        # Return the size of the largest group that doesn't touch the edge (ie is infinite).
        return max(
            len(points) for points in controls.values()
            if all(x != min_x and x != max_x and y != min_y and y != max_y for x, y in points)
        )

    """Return the number of safe locations."""
    distance = 32 if testing else 10000
    return sum(
        sum(abs(x - px) + abs(y - py) for px, py in data) < distance
        for x in range(min_x, max_x + 1)
        for y in range(min_y, max_y + 1)
    )


SAMPLE = """\
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""
TESTS = [(1, SAMPLE, 17), (2, SAMPLE, 16)]
# vim:expandtab:sw=4:ts=4
