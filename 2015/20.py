#!/bin/python
"""Advent of Code, Day 20: Infinite Elves and Infinite Houses."""

import itertools
import functools
import math
import re

import typer
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

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=4),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=8),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_one_int

    def part1(self, parsed_input: InputType) -> int:
        target = parsed_input // 10

        limit = 1000000
        houses = [1] * limit
        for i in range(2, limit):
            for house in range(i, limit, i):
                houses[house] += i

        for i, num in enumerate(houses):
            if num >= target:
                return i

        raise RuntimeError

    def part2(self, parsed_input: InputType) -> int:
        target = parsed_input // 11

        limit = 1000000
        houses = [1] * limit
        for i in range(2, limit):
            for house in range(i, min(limit, i * 51), i):
                houses[house] += i

        for i, num in enumerate(houses):
            if num >= target:
                return i

        raise RuntimeError

    def part1_nope_a(self, parsed_input: InputType) -> int:
        global primes
        if not primes:
            self.pre_run()
        target = parsed_input // 10 - 1

        for i in range(1, 1000000):
            pfactors = prime_factors(i)
            factors = set(pfactors)
            for l in range(2, len(pfactors)):
                factors.update(self.mult(c) for c in itertools.combinations(pfactors, l))

            amount = sum(factors) + 1 + i
            if amount >= target:
                return i
        raise RuntimeError

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

    # def line_parser(self, line: str):
    #     pass


if __name__ == "__main__":
    typer.run(Day20().run)

# vim:expandtab:sw=4:ts=4
