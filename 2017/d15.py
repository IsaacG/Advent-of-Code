#!/bin/python
"""Advent of Code, Day 15: Dueling Generators."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

FACTOR_A = 16807
FACTOR_B = 48271
MOD = 2147483647
MASK = (1 << 16) - 1
SAMPLE = ['65\n8921']

LineType = int
InputType = list[LineType]


class Day15(aoc.Challenge):
    """Day 15: Dueling Generators."""

    PARAMETERIZED_INPUTS = [False, True]
    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=588),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=309),
    ]
    INPUT_PARSER = aoc.parse_ints_per_line

    def solver(self, parsed_input: list[list[int]], param: bool) -> int:
        (val_a,), (val_b,) = parsed_input
        part_two = param
        part_one = not part_two

        def gen(value, factor, mask):
            while True:
                value = value * factor % MOD
                if part_one or value & mask == 0:
                    yield value & MASK

        gen_a = gen(val_a, FACTOR_A, 4 - 1)
        gen_b = gen(val_b, FACTOR_B, 8 - 1)

        return sum(
            1
            for step in range(40_000_000 if part_one else 5_000_000)
            if next(gen_a) == next(gen_b)
        )

# vim:expandtab:sw=4:ts=4
