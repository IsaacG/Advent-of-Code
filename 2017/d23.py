#!/bin/python
"""Advent of Code, Day 23: Coprocessor Conflagration."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
]

LineType = int
InputType = list[LineType]


class Day23(aoc.Challenge):
    """Day 23: Coprocessor Conflagration."""

    TESTS = [
        aoc.TestCase(part=1, inputs="", want=aoc.TEST_SKIP),
        aoc.TestCase(part=2, inputs="", want=None),
    ]

    INPUT_PARSER = aoc.parse_multi_mixed_per_line

    def part1(self, puzzle_input: InputType) -> int:
        code = puzzle_input
        ptr = 0
        mul_count = 0
        registers = {i: 0 for i in "abcdefgh"}

        def val(register: int | str) -> int:
            """Return a value, either an immediate value or register lookup."""
            if isinstance(register, int):
                return register
            return registers[register]

        for step in range(1000000):
            if step and not step % 10000:
                print(step)
            try:
                instructions = code[ptr]
            except:
                return mul_count
            ptr += 1
            match instructions:
                case ["set", str(X), Y]:
                    registers[X] = val(Y)
                case ["sub", str(X), Y]:
                    registers[X] -= val(Y)
                case ["mul", str(X), Y]:
                    mul_count += 1
                    registers[X] *= val(Y)
                case ["jnz", X, Y] if val(X) != 0:
                    ptr += val(Y) - 1
        raise RuntimeError("No solution found.")

    def part2(self, puzzle_input: InputType) -> int:
        return sum(
            1
            for b in range(105700, 122700 + 1, 17)
            if any(b % i == 0 for i in range(2, math.ceil(math.sqrt(b))))
        )

# vim:expandtab:sw=4:ts=4
