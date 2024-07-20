#!/bin/python
"""Advent of Code, Day 13: Packet Scanners."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
0: 3
1: 2
4: 4
6: 4""",
]

LineType = int
InputType = list[LineType]


class Day13(aoc.Challenge):
    """Day 13: Packet Scanners."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=24),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=10),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_ints_per_line

    def part1(self, parsed_input: InputType) -> int:
        ranges = dict(parsed_input)
        positions = {scanner: 0 for scanner in ranges}
        direction = {scanner: 1 for scanner in ranges}
        size = max(ranges) + 1
        severity = 0
        for depth in range(size):
            if depth in positions and positions[depth] == 0:
                severity += ranges[depth] * depth
            positions = {scanner: (position + direction[scanner]) for scanner, position in positions.items()}
            for scanner, range_ in ranges.items():
                if positions[scanner] in (0, range_ - 1):
                    direction[scanner] *= -1

        return severity

    def part2(self, parsed_input: InputType) -> int:
        depths, ranges = [], []
        for depth, range_ in sorted(parsed_input):
            depths.append(depth)
            ranges.append(range_)
        positions = [
            itertools.cycle(list(range(n)) + list(range(n - 2, 0, -1)))
            for n in ranges
        ]

        for depth, position in zip(depths, positions):
            for _ in range(depth):
                next(position)

        for offset in itertools.count():
            if offset % 300000 == 0:
                print(offset)
            locations = [next(position) for position in positions]
            # print(locations)
            if all(locations):
                return offset


    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

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
