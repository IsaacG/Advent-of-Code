#!/bin/python
"""Advent of Code, Day 6: Probably a Fire Hazard. Toggle lights then count them up."""

import re
from lib import aoc


def solve(data: list[tuple[str, int, int, int, int]], part: int) -> int:
    """Return how many lights are on or the levels after toggling them."""
    grid = []
    for i in range(1000):
        grid.append([0] * 1000)
    for action, x1, y1, x2, y2 in data:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if part == 1:
                    match action:
                        case "turn on":
                            grid[x][y] = 1
                        case "toggle":
                            grid[x][y] = 1 - grid[x][y]
                        case "turn off":
                            grid[x][y] = 0
                else:
                    match action:
                        case "turn on":
                            grid[x][y] += 1
                        case "toggle":
                            grid[x][y] += 2
                        case "turn off":
                            grid[x][y] = max(0, grid[x][y] - 1)
    return sum(i for row in grid for i in row)


PARSER = aoc.parse_re_findall_mixed(re.compile(r"turn on|turn off|toggle|\d+"))
TESTS = [
    (1, "turn on 0,0 through 999,999", 1000000),
    (1, "toggle 0,0 through 999,0", 1000),
    (1, "turn on 0,0 through 999,999\ntoggle 0,0 through 999,0", 1000000 - 1000),
    (1, "turn on 0,0 through 999,999\nturn off 0,0 through 999,0", 1000000 - 1000),
    (2, "turn on 0,0 through 999,999", 1000000),
]
