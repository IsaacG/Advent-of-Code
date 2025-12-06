#!/bin/python
"""Advent of Code, Day 6: Trash Compactor."""
from __future__ import annotations

import collections
import functools
import itertools
import logging
import math
import re

from lib import aoc

SAMPLE = [
    """\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +""",  # 2
]

LineType = int
InputType = list[LineType]
log = logging.info


class Day06(aoc.Challenge):
    """Day 6: Trash Compactor."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=4277556),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=3263827),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    # INPUT_PARSER = aoc.parse_ints
    INPUT_PARSER = aoc.parse_one_str
    # INPUT_PARSER = aoc.parse_one_str_per_line
    # INPUT_PARSER = aoc.parse_multi_str_per_line
    # INPUT_PARSER = aoc.parse_one_int
    # INPUT_PARSER = aoc.parse_one_int_per_line
    # INPUT_PARSER = aoc.parse_ints_one_line
    # INPUT_PARSER = aoc.parse_ints_per_line
    # INPUT_PARSER = aoc.parse_re_group_str(r"(a) .* (b) .* (c)")
    # INPUT_PARSER = aoc.parse_re_findall_str(r"(a|b|c)")
    # INPUT_PARSER = aoc.parse_multi_mixed_per_line
    # INPUT_PARSER = aoc.parse_re_group_mixed(r"(foo) .* (\d+)")
    # INPUT_PARSER = aoc.parse_re_findall_mixed(r"\d+|foo|bar")
    # INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_re_findall_int(r"\d+")])
    # INPUT_PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
    # INPUT_PARSER = aoc.CoordinatesParser(chars=None, origin_top_left=True)
    # ---
    # (width, height), start, garden, rocks = puzzle_input
    # max_x, max_y = width - 1, height - 1

    def part1(self, puzzle_input: InputType) -> int:
        puzzle_input = aoc.parse_multi_str_per_line.parse(puzzle_input)
        numbers = [
            [int(i) for i in line]
            for line in puzzle_input[:-1]
        ]
        numbers = list(zip(*numbers))
        total = 0
        for nums, op in zip(numbers, puzzle_input[-1]):
            if op == "+":
                total += sum(nums)
            else:
                total += math.prod(nums)
        return total

    def part2(self, puzzle_input: InputType) -> int:
        *nums, ops = puzzle_input.splitlines()
        starts = [idx for idx, char in enumerate(ops) if char != " "]
        ends = [i - 1 for i in starts[1:]] + [max(len(i) for i in nums)]
        total = 0
        operators = [i for i in ops if i != " "]
        # print(starts, ends, operators)
        for start, end, op in zip(starts, ends, operators):
            numbers = []
            for col in range(start, end):
                number = ""
                for line in nums:
                    if line[col] != " ":
                        number += line[col]
                numbers.append(int(number))
            # print(numbers, op)
            if op == "+":
                total += sum(numbers)
            else:
                total += math.prod(numbers)
        return total



    # def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:

# vim:expandtab:sw=4:ts=4
