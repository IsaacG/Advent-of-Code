#!/bin/python
"""Advent of Code, Day 4: Ceres Search."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""",  # 5
    'XMAS',  # 6
    'XMAS',  # 7
    '.',  # 8
    """\
....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX""",  # 9
    'XMAS',  # 10
]

LineType = int
InputType = list[LineType]


class Day04(aoc.Challenge):
    """Day 4: Ceres Search."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=18),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=9),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.char_map

    def part1(self, puzzle_input: InputType) -> int:
        count = 0
        for coord, letter in puzzle_input.items():
            if letter != "X":
                continue
            for direction in aoc.EIGHT_DIRECTIONS:
                if (
                    puzzle_input.get(coord + 1 * direction) == "M"
                    and puzzle_input.get(coord + 2 * direction) == "A"
                    and puzzle_input.get(coord + 3 * direction) == "S"
                ):
                    count += 1
        return count

    def part2(self, puzzle_input: InputType) -> int:
        count = 0
        for coord, letter in puzzle_input.items():
            if letter != "M":
                continue
            for rotate in (1j ** i for i in range(4)):
                if (
                    puzzle_input.get(coord + 2j * rotate) == "M"
                    and puzzle_input.get(coord + (1 + 1j) * rotate) == "A"
                    and puzzle_input.get(coord + (2 + 2j) * rotate) == "S"
                    and puzzle_input.get(coord + (2) * rotate) == "S"
                ):
                    count += 1
        return count


    # def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:

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

# vim:expandtab:sw=4:ts=4
