#!/bin/python
"""Advent of Code, Day 15: Beacon Exclusion Zone."""
from __future__ import annotations

import dataclasses
import collections
import functools
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

LineType = int
InputType = list[LineType]


def mdist(ax, ay, bx, by) -> int:
    return abs(ax - bx) + abs(ay - by)


@dataclasses.dataclass
class Sensor:
    sx: int
    sy: int
    bx: int
    by: int

    def __post_init__(self):
        self.dist = abs(self.sx - self.bx) + abs(self.sy - self.by)

    def __lt__(self, other):
        return self.sx < other.sx

    def add(self, px, py):
        pdist = mdist(self.sx, self.sy, px, py)
        if pdist > self.dist:
            return px, False
        ydist = abs(self.sy - py)
        right_edge = self.sx + self.dist - ydist
        # print(f"{point} is within {self.sx, self.sy} d:{self.dist} ==> {right_edge}")
        return right_edge + 1, True


class Day15(aoc.Challenge):
    """Day 15: Beacon Exclusion Zone."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=26),
        aoc.TestCase(inputs=SAMPLE, part=2, want=56000011),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_re_findall_int(r"-?\d+")

    def part1(self, parsed_input: InputType) -> int:
        row = 10 if self.testing else 2000000
        positions = set()
        for sx, sy, bx, by in parsed_input:
            dist = mdist(sx, sy, bx, by)
            ydist = abs(row - sy)
            if ydist > dist:
                continue
            startx = sx - (dist - ydist)
            endx = sx + (dist - ydist)
            for i in range(startx, endx):
                positions.add(i)
        return len(positions)

    def part2(self, parsed_input: InputType) -> int:
        dims = 20 if self.testing else 4000000
        sensors = []
        for sx, sy, bx, by in parsed_input:
            sensors.append(Sensor(sx, sy, bx, by))
        sensors.sort()

        # s = Sensor(8, 7, 2, 10)
        # print(s, s + (5, 0), s + (6, 0))

        for cury in range(dims + 1):
            if cury % 100000 == 0:
                print(f"Row {cury}")
            curx = 0
            for s in sensors:
                curx, changed = s.add(curx, cury)
            if curx <= dims:
                print(f"Solved!!! {curx, cury}")
                return curx * 4000000 + cury


    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().input_parser(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]
        # Words: mixed str and int
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in line.split()
            )
            for line in puzzle_input.splitlines()
        ]
        # Regex splitting
        patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in patt.match(line).groups()
            )
            for line in puzzle_input.splitlines()
        ]

    # def line_parser(self, line: str):
    #     pass


if __name__ == "__main__":
    typer.run(Day15().run)

# vim:expandtab:sw=4:ts=4
