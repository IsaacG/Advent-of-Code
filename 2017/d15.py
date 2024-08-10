#!/bin/python
"""Advent of Code, Day 15: Dueling Generators."""

import more_itertools
import itertools
from lib import aoc

FACTOR_A = 16807
FACTOR_B = 48271
MOD = 2147483647
MASK = (1 << 16) - 1
SAMPLE = '65\n8921'


class Day15(aoc.Challenge):
    """Day 15: Dueling Generators."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=588),
        aoc.TestCase(part=2, inputs=SAMPLE, want=309),
    ]
    PARAMETERIZED_INPUTS = [True, False]
    INPUT_PARSER = aoc.parse_ints_per_line

    def solver(self, parsed_input: list[list[int]], param: bool) -> int:
        """Count the number of generated pairs that have matching ends.

        NUC + cpython: 60s
        Desktop + pypy: 3s
        """
        ((val_a,), (val_b,)), part_one = parsed_input, param

        def gen(value, factor, mask):
            while True:
                value = value * factor % MOD
                if part_one or value & mask == 0:
                    yield value & MASK

        gen_a = gen(val_a, FACTOR_A, 4 - 1)
        gen_b = gen(val_b, FACTOR_B, 8 - 1)
        steps = 40_000_000 if part_one else 5_000_000
        pairs = itertools.islice(zip(gen_a, gen_b), steps)
        return sum(for val_a, val_b in pairs if val_a == val_b)

# vim:expandtab:sw=4:ts=4
