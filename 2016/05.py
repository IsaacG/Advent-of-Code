#!/bin/python
"""Advent of Code, Day 5: How About a Nice Game of Chess?."""
from __future__ import annotations

import collections
import functools
import hashlib
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    'abc',  # 1
    '18f47a30',  # 10
    '05ace8e3',
]

LineType = int
InputType = list[LineType]


class Day05(aoc.Challenge):
    """Day 5: How About a Nice Game of Chess?."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=SAMPLE[1]),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=SAMPLE[2]),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_one_str

    def part1(self, parsed_input: InputType) -> int:
        out = []
        base = hashlib.md5(parsed_input.encode())
        for i in itertools.count():
            if i and i % 1000000 == 0:
                self.debug(f"{i=}")
            md5 = base.copy()
            md5.update(str(i).encode())
            digest = md5.hexdigest()
            if digest.startswith("00000"):
                out.append(digest[5])
                self.debug(f"{out=}")
                if len(out) == 8:
                    return "".join(out)

    def part2(self, parsed_input: InputType) -> int:
        out = {}
        base = hashlib.md5(parsed_input.encode())
        for i in itertools.count():
            if i and i % 5000000 == 0:
                self.debug(f"{i=}, {out=}")
            md5 = base.copy()
            md5.update(str(i).encode())
            digest = md5.hexdigest()
            if digest.startswith("00000"):
                pos = digest[5]
                char = digest[6]
                self.debug(f"Found, {i=}, {pos=}, {char=}")
                if pos.isdigit() and int(pos) < 8:
                    out.setdefault(int(pos), char)
                if len(out) == 8:
                    return "".join(out[i] for i in range(8))

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
