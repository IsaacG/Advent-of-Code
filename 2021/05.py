#!/bin/python

"""Advent of Code: Day 05."""

import collections
import dataclasses
import functools
import math
import re
import typer
from typing import Any, Callable

from lib import aoc

SAMPLE = ["""\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""
]

@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def line(self, other: "Point") -> list["Point"]:
        if self.x == other.x:
            return [
                Point(self.x, y)
                for y in range(min(self.y, other.y), max(self.y, other.y) + 1)
            ]
        if self.y == other.y:
            return [
                Point(x, self.y)
                for x in range(min(self.x, other.x), max(self.x, other.x) + 1)
            ]
        if abs(self.x - other.x) != abs(self.y - other.y):
            raise RuntimeError("Not 90 nor 45 degrees")
        count = abs(self.x - other.x) + 1
        dir_x = 1 if other.x > self.x else -1
        dir_y = 1 if other.y > self.y else -1
        return [
            Point(self.x + dir_x * i, self.y + dir_y * i)
            for i in range(count)
        ]


# A list of point->point pairs, delineating a line.
InputType = list[tuple[Point, Point]]


class Day05(aoc.Challenge):
    """Map where geothermal vent clouds cross paths."""

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=5),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=12),
    )

    def part1(self, lines: InputType) -> int:
        """Find hot areas where lines overlap. Ignore diagonals."""
        lines = [l for l in lines if l[0].x == l[1].x or l[0].y == l[1].y]
        return self.part2(lines)

    def part2(self, lines: InputType) -> int:
        """Find hot areas where lines overlap. Include diagonals."""
        points = []
        count = collections.Counter()
        for start, end in lines:
            count.update(start.line(end))

        return len([1 for v in count.values() if v > 1])

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [
            tuple(
                Point(*list(int(i) for i in part.split(",")))
                for part in line.split(" -> ")
            )
            for line in puzzle_input.splitlines()
        ]


if __name__ == "__main__":
    typer.run(Day05().run)
