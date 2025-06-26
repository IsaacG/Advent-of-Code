#!/bin/python
"""Advent of Code, Day 20: Infinite Elves and Infinite Houses."""

import itertools
import functools
import math
import re

from lib import aoc

SAMPLE = ["70", "130"]

LineType = int
InputType = list[LineType]

primes = None

@functools.cache
def prime_factors(num: int) -> list[int]:
    factors = []
    for p in primes:
        if p * p > num:
            return []
        if num % p == 0:
            return prime_factors(num // p) + [p]
    raise RuntimeError


class Day20(aoc.Challenge):
    """Day 20: Infinite Elves and Infinite Houses."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=4),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=8),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, puzzle_input: InputType) -> int:
        target = puzzle_input // 10

        limit = 1000000
        houses = [1] * limit
        for i in range(2, limit):
            for house in range(i, limit, i):
                houses[house] += i

        for i, num in enumerate(houses):
            if num >= target:
                return i

        raise RuntimeError

    def part2(self, puzzle_input: InputType) -> int:
        target = puzzle_input // 11

        limit = 1000000
        houses = [1] * limit
        for i in range(2, limit):
            for house in range(i, min(limit, i * 51), i):
                houses[house] += i

        for i, num in enumerate(houses):
            if num >= target:
                return i

        raise RuntimeError

    def part1_nope_a(self, puzzle_input: InputType) -> int:
        global primes
        if not primes:
            self.pre_run()
        target = puzzle_input // 10 - 1

        for i in range(1, 1000000):
            pfactors = prime_factors(i)
            factors = set(pfactors)
            for l in range(2, len(pfactors)):
                factors.update(math.prod(c) for c in itertools.combinations(pfactors, l))

            amount = sum(factors) + 1 + i
            if amount >= target:
                return i
        raise RuntimeError
