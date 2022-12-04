#!/bin/python
"""Advent of Code: Day 06."""

from __future__ import annotations

import collections
import dataclasses
import functools
import math
import re
from typing import Optional

import typer
from lib import aoc

SAMPLE = [
    "turn on 0,0 through 999,999",
    "toggle 0,0 through 999,0",
    "turn on 0,0 through 999,999\ntoggle 0,0 through 999,0",
    "turn on 0,0 through 999,999\nturn off 0,0 through 999,0",
]
PARSE_RE = re.compile(r"^(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)$")


@dataclasses.dataclass
class Point:
    x: int
    y: int

@dataclasses.dataclass
class Rect:

    start: Point
    end: Point

    def __post_init__(self) -> None:
        if self.start.x > self.end.x:
            self.start.x, self.end.x = self.end.x, self.start.x
        if self.start.y > self.end.y:
            self.start.y, self.end.y = self.end.y, self.start.y

    def area(self) -> int:
        return abs(self.end.x - self.start.x + 1) * abs(self.end.y - self.start.y + 1)

    def overlap(self, other: Rect) -> Optional[Rect]:
        if other.end.x < self.start.x or other.end.y < self.start.y:
            return None
        if other.start.x > self.end.x or other.start.x > self.end.y:
            return None
        start = Point(max(self.start.x, other.start.x), max(self.start.y, other.start.y))
        end = Point(min(self.end.x, other.end.x), min(self.end.y, other.end.y))
        return Rect(start, end)


InputType = tuple[str, Rect]


class Day06(aoc.Challenge):
    """Day 6: Probably a Fire Hazard."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=1000000),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=1000),
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=1000000 - 1000),
        aoc.TestCase(inputs=SAMPLE[3], part=1, want=1000000 - 1000),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=1000000),
    )

    def part1_overlaps(self, parsed_input: InputType) -> int:
        add = []
        sub = []
        for count, (action, rect) in enumerate(parsed_input):
            if count % 50 == 0:
                print(count, len(add), len(sub))
            match action:
                case "turn on":
                    new_add, new_sub = [rect], []
                    for i in add:
                        overlap = rect.overlap(i)
                        if overlap:
                            new_sub.append(overlap)
                    for i in sub:
                        overlap = rect.overlap(i)
                        if overlap:
                            new_add.append(overlap)
                    add.extend(new_add)
                    sub.extend(new_sub)
                case "toggle":
                    for i in add:
                        overlap = rect.overlap(i)
                        if overlap:
                            sub.append(overlap)
                            sub.append(overlap)
                    add.append(rect)
                case "turn off":
                    for i in add:
                        overlap = rect.overlap(i)
                        if overlap:
                            sub.append(overlap)
        area_add = sum(i.area() for i in add) 
        area_sub = sum(i.area() for i in sub)
        self.debug(f"{area_add=} {area_sub=}")
        return area_add - area_sub

    def part1(self, parsed_input: InputType) -> int:
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
        t = sum(i for row in grid for i in row)
        assert t > 322000
        return t

    def part2(self, parsed_input: InputType) -> int:
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

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        out = []
        for i in puzzle_input.splitlines():
            action, *nums = PARSE_RE.match(i).groups()
            out.append((action,) + tuple(int(i) for i in nums))
        return out


if __name__ == "__main__":
    typer.run(Day06().run)

# vim:expandtab:sw=4:ts=4
