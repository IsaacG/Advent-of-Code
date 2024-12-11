#!/bin/python
"""Advent of Code, Day 11: Plutonian Pebbles."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
125 17""",
]

LineType = int
InputType = list[LineType]


class Day11(aoc.Challenge):
    """Day 11: Plutonian Pebbles."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=55312),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    @functools.cache
    def count_stone(self, stone: int, steps: int) -> int:
        if steps == 0:
            return 1
        if stone == 0:
            return self.count_stone(1, steps - 1)
        stone_str = str(stone)
        stone_len = len(stone_str)
        if stone_len % 2 == 0:
            a = int(stone_str[:stone_len // 2])
            b = int(stone_str[stone_len // 2:])
            return self.count_stone(a, steps - 1) + self.count_stone(b, steps - 1)
        return self.count_stone(stone * 2024, steps - 1)

    def p1(self, steps) -> int:
        stones = [1]
        for i in range(steps):
            new = []
            for stone in stones:
                stone_str = str(stone)
                stone_len = len(stone_str)
                if stone == 0:
                    new.append(1)
                elif stone_len % 2 == 0:
                    new.append(int(stone_str[:stone_len // 2]))
                    new.append(int(stone_str[stone_len // 2:]))
                else:
                    new.append(stone * 2024)
            stones = new
            # print(i + 1, len(stones), stones)
        return len(stones)

    def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:
        steps = 25 if part_one else 75
        return sum(self.count_stone(stone, steps) for stone in puzzle_input)

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
