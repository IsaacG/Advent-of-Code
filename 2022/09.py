#!/bin/python
"""Advent of Code, Day 9: Rope Bridge."""

import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = [
    """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""","""\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""","""
..T...
...H..
......
......
s.....

......
...TH.
......
......
s.....

......
....TH
......
......
s.....

== D 1 ==

......
....T.
.....H
......
s.....

== L 5 ==

......
....T.
....H.
......
s.....

......
....T.
...H..
......
s.....

......
......
..HT..
......
s.....

......
......
.HT...
......
s.....

......
......
HT....
......
s.....

== R 2 ==

......
......
.H....  (H covers T)
......
s.....

......
......
.TH...
......
s.....""",  # 7
    's',  # 8
    '#',  # 9
    """\
..##..
...##.
.####.
....#.
s###..""",  # 10
]

LineType = int
InputType = list[LineType]


class Day09(aoc.Challenge):
    """Day 9: Rope Bridge."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=13),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=36),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    # Convert lines to type:
    INPUT_TYPES = LineType
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        DIAG = [ ((1 + 1j) * -1j ** i) for i in range(4)]
        DIR = aoc.DIRECTIONS
        BOTH = DIAG + DIR
        points = set([0])
        head = 0
        tail = 0
        for direction, unit in parsed_input:
            for _ in range(unit):
                match direction:
                    case "R":
                            head += 1
                    case "L":
                            head -= 1
                    case "U":
                            head += 1j
                    case "D":
                            head -= 1j
                if head - tail in BOTH:
                    continue
                x = 0
                if head.real > tail.real:
                    x = 1
                if head.real < tail.real:
                    x = -1
                y = 0
                if head.imag > tail.imag:
                    y = 1
                if head.imag < tail.imag:
                    y = -1
                tail += complex(x, y)
                points.add(tail)
        return len(points)

    def part2(self, parsed_input: InputType) -> int:
        DIAG = [ ((1 + 1j) * -1j ** i) for i in range(4)]
        DIR = aoc.DIRECTIONS
        BOTH = DIAG + DIR
        points = set([0])
        knots = [0] * 10
        for direction, unit in parsed_input:
            for _ in range(unit):
                match direction:
                    case "R":
                            knots[0] += 1
                    case "L":
                            knots[0] -= 1
                    case "U":
                            knots[0] += 1j
                    case "D":
                            knots[0] -= 1j
                for i, (a, b) in enumerate(zip(knots, knots[1:])):
                    if a - b in BOTH:
                        continue
                    x = 0
                    if a.real > b.real:
                        x = 1
                    if a.real < b.real:
                        x = -1
                    y = 0
                    if a.imag > b.imag:
                        y = 1
                    if a.imag < b.imag:
                        y = -1
                    knots[i + 1] += complex(x, y)
                points.add(knots[-1])
        return len(points)



    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in line.split()
            )
            for line in puzzle_input.splitlines()
        ]

    # def line_parser(self, line: str):
    #     pass


if __name__ == "__main__":
    typer.run(Day09().run)

# vim:expandtab:sw=4:ts=4
