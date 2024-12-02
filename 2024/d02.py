#!/bin/python
"""Advent of Code, Day 2: Red-Nosed Reports."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""",  # 0
    '7 6 4 2 1',  # 1
    '1 2 7 8 9',  # 2
    '2 7',  # 3
    '9 7 6 2 1',  # 4
    '6 2',  # 5
    '1 3 2 4 5',  # 6
    '1 3',  # 7
    '3 2',  # 8
    '8 6 4 4 1',  # 9
    '4 4',  # 10
    '1 3 6 7 9',  # 11
]

LineType = int
InputType = list[LineType]


class Day02(aoc.Challenge):
    """Day 2: Red-Nosed Reports."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=2),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=4),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    # INPUT_PARSER = aoc.parse_one_str
    # INPUT_PARSER = aoc.parse_one_str_per_line
    # INPUT_PARSER = aoc.parse_multi_str_per_line
    # INPUT_PARSER = aoc.parse_one_int
    # INPUT_PARSER = aoc.parse_one_int_per_line
    # INPUT_PARSER = aoc.parse_ints_one_line
    INPUT_PARSER = aoc.parse_ints_per_line
    # INPUT_PARSER = aoc.parse_re_group_str(r"(a) .* (b) .* (c)")
    # INPUT_PARSER = aoc.parse_re_findall_str(r"(a|b|c)")
    # INPUT_PARSER = aoc.parse_multi_mixed_per_line
    # INPUT_PARSER = aoc.parse_re_group_mixed(r"(foo) .* (\d+)")
    # INPUT_PARSER = aoc.parse_re_findall_mixed(r"\d+|foo|bar")
    # INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_re_findall_int(r"\d+")])
    # INPUT_PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
    # INPUT_PARSER = aoc.AsciiBoolMapParser("#")
    # ---
    # INPUT_PARSER = aoc.CharCoordinatesParser("S.#")
    # (width, height), start, garden, rocks = puzzle_input
    # max_x, max_y = width - 1, height - 1

    def part1(self, puzzle_input: InputType) -> int:
        count = 0
        for line in puzzle_input:
            increase = line[1] > line[0]
            if increase and any(a > b for a, b in zip(line, line[1:])):
                continue
            if (not increase) and any(a < b for a, b in zip(line, line[1:])):
                continue
            if not all(1 <= abs(a - b) <= 3 for a, b in zip(line, line[1:])): 
                continue
            count += 1
        return count

    def safe(self, line) -> bool:
        increase = line[1] > line[0]
        if increase and any(a > b for a, b in zip(line, line[1:])):
            return False
        if (not increase) and any(a < b for a, b in zip(line, line[1:])):
            return False
        if not all(1 <= abs(a - b) <= 3 for a, b in zip(line, line[1:])): 
            return False
        return True

    def part2(self, puzzle_input: InputType) -> int:
        count = 0
        for line in puzzle_input:
            for i in range(len(line)):
                part = line[:i] + line[1+i:]
                if self.safe(part):
                    count += 1
                    break
        return count


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
