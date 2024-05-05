#!/bin/python
"""Advent of Code: Day 06."""

import re

from lib import aoc

SAMPLE = [
    "turn on 0,0 through 999,999",
    "toggle 0,0 through 999,0",
    "turn on 0,0 through 999,999\ntoggle 0,0 through 999,0",
    "turn on 0,0 through 999,999\nturn off 0,0 through 999,0",
]
PARSE_RE = re.compile(r"turn on|turn off|toggle|\d+")


LineType = tuple[str, int, int, int, int]
InputType = list[LineType]


class Day06(aoc.Challenge):
    """Day 6: Probably a Fire Hazard. Toggle lights then count them up."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=1000000),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=1000),
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=1000000 - 1000),
        aoc.TestCase(inputs=SAMPLE[3], part=1, want=1000000 - 1000),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=1000000),
    ]
    INPUT_PARSER = aoc.parse_re_findall_mixed(PARSE_RE)

    def part1(self, parsed_input: InputType) -> int:
        """Return how many lights are on after toggling them."""
        grid = []
        for i in range(1000):
            grid.append([False] * 1000)
        for action, x1, y1, x2, y2 in parsed_input:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    match action:
                        case "turn on":
                            grid[x][y] = True
                        case "toggle":
                            grid[x][y] = not grid[x][y]
                        case "turn off":
                            grid[x][y] = False
                        case _:
                            raise ValueError(f"Unknown {action=}")
        return sum(i for row in grid for i in row)

    def part2(self, parsed_input: InputType) -> int:
        """Return light levels after toggling them."""
        grid = []
        for i in range(1000):
            grid.append([0] * 1000)
        for action, x1, y1, x2, y2 in parsed_input:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    match action:
                        case "turn on":
                            grid[x][y] += 1
                        case "toggle":
                            grid[x][y] += 2
                        case "turn off":
                            grid[x][y] = max(0, grid[x][y] - 1)
                        case _:
                            raise ValueError(f"Unknown {action=}")
        return sum(i for row in grid for i in row)
