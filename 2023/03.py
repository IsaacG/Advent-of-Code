#!/bin/python
"""Advent of Code, Day 3: Gear Ratios."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""",  # 1
]

LineType = int
InputType = list[LineType]


class Day03(aoc.Challenge):
    """Day 3: Gear Ratios."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=4361),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=467835),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    # INPUT_PARSER = aoc.parse_one_str_per_line
    # INPUT_PARSER = aoc.parse_one_str
    # INPUT_PARSER = aoc.parse_one_int
    # INPUT_PARSER = aoc.parse_one_str_per_line
    # INPUT_PARSER = aoc.parse_one_int_per_line
    # INPUT_PARSER = aoc.parse_multi_str_per_line
    # INPUT_PARSER = aoc.parse_re_group_str(r"(a) .* (b) .* (c)")
    # INPUT_PARSER = aoc.parse_re_findall_str(r"(a|b|c)")
    # INPUT_PARSER = aoc.parse_multi_int_per_line
    # INPUT_PARSER = aoc.parse_re_group_int(r"(\d+)")
    # INPUT_PARSER = aoc.parse_re_findall_int(r"\d+")
    # INPUT_PARSER = aoc.parse_multi_mixed_per_line
    # INPUT_PARSER = aoc.parse_re_group_mixed(r"(foo) .* (\d+)")
    # INPUT_PARSER = aoc.parse_re_findall_mixed(r"\d+|foo|bar")
    # INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_re_findall_int(r"\d+")])
    # INPUT_PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
    # INPUT_PARSER = aoc.parse_ascii_bool_map("#")

    def part1(self, parsed_input: InputType) -> int:
        number, number_pos, items = parsed_input
        neighbors = {
            neighbor
            for pos in items
            for neighbor in aoc.neighbors(pos, directions=aoc.EIGHT_DIRECTIONS)
        }
        all_nums = {
            number_pos[neighbor]
            for neighbor in neighbors
            if neighbor in number_pos
        }
        res = sum(number[pos] for pos in all_nums)
        assert res != 568651
        return res

    def part2(self, parsed_input: InputType) -> int:
        number, number_pos, items = parsed_input
        total = 0
        for pos, char in items.items():
            if char == "*":
                neighbors = aoc.neighbors(pos, directions=aoc.EIGHT_DIRECTIONS)
                nums = {
                    number_pos[neighbor]
                    for neighbor in neighbors
                    if neighbor in number_pos
                }
                if len(nums) == 2:
                    total += math.prod(number[pos] for pos in nums)
        return total

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        numbers = {}
        number_pos = {}
        items = {}
        for y, line in enumerate(puzzle_input.splitlines()):
            for match in re.finditer(r"\d+", line):
                x1, x2 = match.span()
                val = int(match.group())
                numbers[complex(x1, y)] = val
                for x in range(x1, x2):
                    number_pos[complex(x, y)] = complex(x1, y)
            for x, char in enumerate(line):
                if not char.isdigit() and char != ".":
                    items[complex(x, y)] = char
        return numbers, number_pos, items


# vim:expandtab:sw=4:ts=4
