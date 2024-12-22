#!/bin/python
"""Advent of Code, Day 22: Monkey Market."""
from __future__ import annotations

import collections
import functools
import itertools
import more_itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
1
10
100
2024""",
    """\
1
2
3
2024"""
]

LineType = int
InputType = list[LineType]


class Day22(aoc.Challenge):
    """Day 22: Monkey Market."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=37327623),
        aoc.TestCase(part=2, inputs=SAMPLE[1], want=23),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]


    def part1(self, puzzle_input: InputType) -> int:

        def rand(number):
            number = (number ^ (number * 64)) % 16777216
            number = (number ^ (number // 32)) % 16777216
            number = (number ^ (number * 2048)) % 16777216
            return number


        total = 0
        for number in puzzle_input:
            secret_number = number

            for _ in range(2000):
                number = rand(number)
            total += number
        return total
        # print("\n".join(["==="] + [f"{k}={v!r}" for k, v in locals().items()] + ["==="]))

    def part2(self, puzzle_input: InputType) -> int:

        def rand(number):
            number = (number ^ (number * 64)) % 16777216
            number = (number ^ (number // 32)) % 16777216
            number = (number ^ (number * 2048)) % 16777216
            return number

        def seq(number):
            yield number % 10
            for _ in range(2000):
                number = rand(number)
                yield number % 10


        total = 0
        sequences = [list(seq(number)) for number in puzzle_input]
        print("Generated sequences")

        seq_deltas = [
            [
                ([b - a for a, b in zip(nums, nums[1:])], nums[-1])
                for nums in [sequence[i:i+5] for i in range(len(sequence) - 4)]
            ]
            for sequence in sequences
        ]
        print("Generated deltas")

        def test(opt):
            return sum(
                next((j for i, j in sq if i == opt), 0)
                for sq in seq_deltas
            )


        def brute():
            m = 0
            for a in range(-9, 10):
                for b in range(-9, 10):
                    print(a, b, m)
                    m = max(m, max(test([a,b,c,d]) for c in range(-9, 10) for d in range(-9, 10)))
            return m

        return brute()

        return total

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
