"""Drone Paths

A delivery drone must fly from the charging station at the top‑left of a city grid to the drop point at the bottom‑right.
Some air zones have turbulence (marked 1) and must be avoided; safe zones are marked 0.
The drone can only move right or down between adjacent safe zones.
Given a grid of 0s and 1s, return the number of distinct safe routes from top‑left to bottom‑right.
"""

import functools


def countDronePaths(grid):
    # return the number of distinct safe routes
    safe = {(x, y) for y, row in enumerate(grid) for x, val in enumerate(row) if val == 0}
    end = max(safe)

    @functools.cache
    def paths(x: int, y: int) -> int:
        if (x, y) == end:
            return 1
        if (x, y) not in safe:
            return 0
        return paths(x + 1, y) + paths(x, y + 1)

    return paths(0, 0)

assert countDronePaths([[0]]) == 1
assert countDronePaths([[0, 1], [0, 0]]) == 1
assert countDronePaths([[0, 0], [0, 0]]) == 2
