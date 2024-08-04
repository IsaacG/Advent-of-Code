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

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=588),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=309),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_ints_per_line

    def part1(self, parsed_input: InputType) -> int:
        (val_a,), (val_b,) = parsed_input
        count = 0
        seen = {}
        for step in range(40_000_000):
            if step and step % 1_000_000 == 0:
                print(step)
            val_a = val_a * FACTOR_A % MOD
            val_b = val_b * FACTOR_B % MOD
            if (val_a & MASK) == (val_b & MASK):
                count += 1

        print("\n".join(["==="] + [f"{k}={v!r}" for k, v in locals().items()] + ["==="]))
        return count

    def part2(self, parsed_input: InputType) -> int:
        (val_a,), (val_b,) = parsed_input

        def gen(value, factor, mask):
            while True:
                value = value * factor % MOD
                if value & mask == 0:
                    yield value & MASK

        count = 0
        gen_a = gen(val_a, FACTOR_A, 4 - 1)
        gen_b = gen(val_b, FACTOR_B, 8 - 1)
        for step in range(5_000_000):
            if next(gen_a) == next(gen_b):
                count += 1

        print("\n".join(["==="] + [f"{k}={v!r}" for k, v in locals().items()] + ["==="]))
        return count

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

# vim:expandtab:sw=4:ts=4
