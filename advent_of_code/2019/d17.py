#!/bin/python
"""Advent of Code, Day 17: Set and Forget."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

import intcode
from lib import aoc

SAMPLE = [
    """\
..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..""",
]

LineType = int
InputType = list[LineType]


class Day17(aoc.Challenge):
    """Day 17: Set and Forget."""

    DEBUG = False
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=aoc.TEST_SKIP),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=0),
    ]

    INPUT_PARSER = aoc.parse_one_str

    def part1(self, puzzle_input: InputType) -> int:
        computer = intcode.Computer(puzzle_input, debug=self.DEBUG)
        computer.run()
        data = [chr(i) for i in computer.output]
        scaffolding = aoc.CoordinatesParserC(chars="#<>^v").parse("".join(data))
        return sum(
            pos.real * pos.imag
            for pos in scaffolding
            if all(pos + direction in scaffolding for direction in aoc.FOUR_DIRECTIONS)
        )

    def part2(self, puzzle_input: InputType) -> int:
        raise NotImplementedError

    def solver(self, puzzle_input: InputType, param: bool) -> int | str:
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
