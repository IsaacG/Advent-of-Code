#!/bin/python
"""Advent of Code, Day 3: Lobby."""
from __future__ import annotations

import collections
import functools
import itertools
import logging
import math
import re

from lib import aoc

SAMPLE = [
    """\
987654321111111
811111111111119
234234234234278
818181911112111""",  # 2
]

LineType = int
InputType = list[LineType]
log = logging.info


class Day03(aoc.Challenge):
    """Day 3: Lobby."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=357),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=3121910778619),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_one_str_per_line

    def part1(self, puzzle_input: InputType) -> int:
        t = 0
        for line in puzzle_input:
            a = max(line[:-1])
            b = max(line[line.index(a)+1:])
            t += int(a+b)
        return t

        print("\n".join(["==="] + [f"{k}={v!r}" for k, v in locals().items()] + ["==="]))
        return None

    def part2(self, puzzle_input: InputType) -> int:
        t = 0
        for line in puzzle_input:
            digits = []
            for i in range(12):
                a = max(line[:-11+i] if i != 11 else line)

                digits.append(a)
                line = line[line.index(a)+1:]

            t += int("".join(digits))
        return t


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
