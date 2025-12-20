#!/bin/python
"""Advent of Code, Day 15: Dueling Generators."""

import itertools

FACTOR_A = 16807
FACTOR_B = 48271
MOD = 2147483647
MASK = (1 << 16) - 1
SAMPLE = '65\n8921'
TIMEOUT = 90


def solve(data: list[list[int]], part: int) -> int:
    """Count the number of generated pairs that have matching ends.

    NUC + cpython: 60s
    Desktop + pypy: 3s
    """
    val_a, val_b = [int(line[-1]) for line in data]

    def gen(value, factor, mask):
        while True:
            value = value * factor % MOD
            if part == 1 or value & mask == 0:
                yield value & MASK

    gen_a = gen(val_a, FACTOR_A, 4 - 1)
    gen_b = gen(val_b, FACTOR_B, 8 - 1)
    steps = 40_000_000 if part == 1 else 5_000_000
    pairs = itertools.islice(zip(gen_a, gen_b), steps)
    return sum(1 for val_a, val_b in pairs if val_a == val_b)


TESTS = [(1, SAMPLE, 588), (2, SAMPLE, 309)]
# vim:expandtab:sw=4:ts=4
