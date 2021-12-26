#!/bin/python
"""Advent of Code: Day 25."""

import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = ["""\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""]
InputType = list[int]
EMPTY = 0
RIGHT = 1
DOWN = 2


class Day25(aoc.Challenge):

    DEBUG = True
    SUBMIT = {1: True, 2: False}

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=58),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=0),
    )

    # Convert lines to type:
    INPUT_TYPES = int
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        board = parsed_input
        max_x = max(x for x, _ in board) + 1
        max_y = max(y for _, y in board) + 1
        right = {k for k, v in board.items() if v == RIGHT}
        down = {k for k, v in board.items() if v == DOWN}
        prior = set()

        next_right = lambda x, y: ((x + 1) % max_x, y)
        next_down = lambda x, y: (x, (y + 1) % max_y)

        def new_set(old_set, next_f, other):
            _new = set()
            for x, y in old_set:
                _point = next_f(x, y)
                if _point in old_set or _point in other:
                    _new.add((x, y))
                else:
                    _new.add(_point)
            return _new

        for step in range(500):
            new = right | down
            if new == prior:
                return step
            prior = new

            right = new_set(right, next_right, down)
            down = new_set(down, next_down, right)
        raise RuntimeError("out of bounds")
            
    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        vals = {".": EMPTY, ">": RIGHT, "v": DOWN}
        return {
            (x, y): vals[val]
            for y, line in enumerate(puzzle_input.splitlines())
            for x, val in enumerate(line)
        }


if __name__ == "__main__":
    typer.run(Day25().run)

# vim:expandtab:sw=4:ts=4
