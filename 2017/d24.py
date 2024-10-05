#!/bin/python
"""Advent of Code, Day 24: Electromagnetic Moat."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10""",  # 8
]

LineType = int
InputType = list[LineType]


class Day24(aoc.Challenge):
    """Day 24: Electromagnetic Moat."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=31),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=19),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    def part1(self, puzzle_input: frozenset[tuple[int, int]]) -> int:
        print("\n".join(["==="] + [f"{k}={v!r}" for k, v in locals().items()] + ["==="]))

        functools.cache
        def strongest(start: int, options: frozenset[tuple[int, int]]) -> int:
            most = 0
            for option in options:
                if start not in option:
                    continue
                other = list(option)
                other.remove(start)
                next_start = other[0]
                value = strongest(next_start, options - {option}) + start + next_start
                most = max(most, value)
            return most

        return strongest(0, puzzle_input)

    def part2(self, puzzle_input: InputType) -> int:

        functools.cache
        def longest(start: int, options: frozenset[tuple[int, int]]) -> int:
            most = 0
            for option in options:
                if start not in option:
                    continue
                other = list(option)
                other.remove(start)
                next_start = other[0]
                value = longest(next_start, options - {option}) + 1
                most = max(most, value)
            return most

        functools.cache
        def strongest(start: int, length: int, options: frozenset[tuple[int, int]]) -> int | None:
            most = 0
            for option in options:
                if start not in option:
                    continue
                other = list(option)
                other.remove(start)
                next_start = other[0]
                value = strongest(next_start, length - 1, options - {option})
                if value is not None:
                    most = max(most, value + start + next_start)
            if most == 0 and length > 0:
                return None
            return most

        length = longest(0, puzzle_input)
        return strongest(0, length, puzzle_input)


    def solver(self, puzzle_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> frozenset[tuple[int, int]]:
        """Parse the input data."""
        lines = puzzle_input.splitlines()
        pairs = {tuple(sorted(int(i) for i in line.split("/"))) for line in lines}
        assert len(pairs) == len(lines)
        return frozenset(pairs)

# vim:expandtab:sw=4:ts=4
