#!/bin/python
"""Advent of Code, Day 3: Mull It Over."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))',
    "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))",
    '%&mul[3,7]!@^do_not_',  # 16
    '+mul(32,64]then(',  # 17
    ')',  # 18
    'mul',  # 19
    '2*4 + 5*5 + 11*8 + 8*5',  # 20
    'mul',  # 21
]

LineType = int
InputType = list[LineType]


class Day03(aoc.Challenge):
    """Day 3: Mull It Over."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=161),
        aoc.TestCase(part=2, inputs=SAMPLE[1], want=48),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_one_str

    def part1(self, puzzle_input: InputType) -> int:
        return sum(
        int(a) * int(b)
        for a, b in re.findall(r"mul\((\d+),(\d+)\)", puzzle_input)
        )

    def part2(self, puzzle_input: InputType) -> int:
        parts = puzzle_input.split("don't()")
        t = [p for p in parts[1:] if "do()" in p]
        t = [p.split("do()", 1)[1] for p in t]
        puzzle_input = parts[0] + "".join(t)
        print(puzzle_input)
        return sum(
        int(a) * int(b)
        for a, b in re.findall(r"mul\((\d+),(\d+)\)", puzzle_input)
        )

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
