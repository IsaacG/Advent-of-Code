#!/bin/python

"""Advent of Code: Day 05."""

import collections
import dataclasses
import itertools
import re
import typer

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
    """A cartesian point."""
    x: int
    y: int


@dataclasses.dataclass(frozen=True)
class Line:
    """A line formed between two cartesian points."""
    start: Point
    end: Point

    def points(self) -> list[Point]:
        """Return the points on the line."""
        if (
            abs(self.start.x - self.end.x) != abs(self.start.y - self.end.y)  # 45 degrees
            and abs(self.start.x - self.end.x) != 0  # vertical
            and abs(self.start.y - self.end.y) != 0  # horizontal
        ):
            raise RuntimeError(f"{self} not 90 nor 45 degrees")

        if self.start == self.end:
            steps = 1
        elif abs(self.start.x - self.end.x) != 0:
            steps = abs(self.start.x - self.end.x)
        else:
            steps = abs(self.start.y - self.end.y)

        dir_x = (self.end.x - self.start.x) / steps
        dir_y = (self.end.y - self.start.y) / steps
        return [
            Point(self.start.x + dir_x * i, self.start.y + dir_y * i)
            for i in range(steps + 1)
        ]


# A list of point->point pairs, delineating a line.
InputType = list[Line]


class Day05(aoc.Challenge):
    """Map where geothermal vent clouds cross paths."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=5),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=12),
    )

    def part1(self, lines: InputType) -> int:
        """Find hot areas where lines overlap. Ignore diagonals."""
        # Filter for horizontal/vertical and call part 2.
        lines = [l for l in lines if l.start.x == l.end.x or l.start.y == l.end.y]
        return self.part2(lines)

    def part2(self, lines: InputType) -> int:
        """Find hot areas where lines overlap. Include diagonals."""
        # Count points that are on lines.
        count = collections.Counter(
            itertools.chain.from_iterable(line.points() for line in lines)
        )
        return sum(1 for v in count.values() if v > 1)

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data.

        Split into lines. Split each line into a `start -> end`.
        Make a tuple(begin, end) Points for each line.
        """
        pattern = re.compile(r'^([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)$')
        lines = []
        for line in puzzle_input.splitlines():
            match = pattern.match(line)
            lines.append(
                Line(
                    Point(int(match.group(1)), int(match.group(2))),
                    Point(int(match.group(3)), int(match.group(4))),
                )
            )
        return lines


if __name__ == "__main__":
    typer.run(Day05().run)
