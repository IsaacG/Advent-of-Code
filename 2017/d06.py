#!/bin/python
"""Advent of Code, Day 6: Memory Reallocation."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = ["0 2 7 0"]

InputType = list[list[int]]


class Day06(aoc.Challenge):
    """Day 6: Memory Reallocation."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=5),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=4),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_multi_int_per_line

    def part1(self, parsed_input: InputType) -> int:
        banks = parsed_input[0].copy()
        seen = set()
        count = len(banks)
        for steps in range(100000):
            # print(steps, banks)
            t = tuple(banks)
            if t in seen:
                return steps
            seen.add(t)
            num, idx = max((num, -idx) for idx, num in enumerate(banks))
            idx = -idx
            # print(f"Select {idx} with {num}")
            banks[idx] = 0
            for bank in range(idx + 1, idx + 1 + num):
                banks[bank % count] += 1

        return 0

    def part2(self, parsed_input: InputType) -> int:
        banks = parsed_input[0].copy()
        seen = {}
        count = len(banks)
        for steps in range(100000):
            # print(steps, banks)
            t = tuple(banks)
            if t in seen:
                return steps - seen[t]
            seen[t] = steps
            num, idx = max((num, -idx) for idx, num in enumerate(banks))
            idx = -idx
            # print(f"Select {idx} with {num}")
            banks[idx] = 0
            for bank in range(idx + 1, idx + 1 + num):
                banks[bank % count] += 1

        return 0

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

# vim:expandtab:sw=4:ts=4
