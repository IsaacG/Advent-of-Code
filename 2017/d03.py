#!/bin/python
"""Advent of Code, Day 3: Spiral Memory."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    '1024',  # 10
]

LineType = int
InputType = list[LineType]


class Day03(aoc.Challenge):
    """Day 3: Spiral Memory."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=31),
        aoc.TestCase(inputs="747", part=2, want=806),
    ]
    PARAMETERIZED_INPUTS = [False, True]
    INPUT_PARSER = aoc.parse_one_int

    def part1(self, parsed_input: InputType) -> int:
        location = complex()
        number = 1
        direction = complex(0, -1)
        rotate_left = 1j

        matrix = {location: number}
        for number in range(2, parsed_input + 1):
            if location + direction * rotate_left not in matrix:
                direction *= rotate_left
            location += direction
            matrix[location] = number

        return int(abs(location.real) + abs(location.imag))

    def part2(self, parsed_input: InputType) -> int:
        location = complex()
        number = 1
        direction = complex(0, -1)
        rotate_left = 1j

        matrix = {location: number}
        for number in range(2, parsed_input + 1):
            if location + direction * rotate_left not in matrix:
                direction *= rotate_left
            location += direction
            value = sum(matrix.get(location + offset, 0) for offset in aoc.EIGHT_DIRECTIONS)
            matrix[location] = value
            if value > parsed_input:
                return value

        raise RuntimeError("Not found")


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
