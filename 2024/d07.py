#!/bin/python
"""Advent of Code, Title."""
from __future__ import annotations

import collections
import operator
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
]

LineType = int
InputType = list[LineType]


class Day07(aoc.Challenge):
    """Title."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=3749),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=11387),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    # INPUT_PARSER = aoc.parse_one_str
    # INPUT_PARSER = aoc.parse_one_str_per_line
    # INPUT_PARSER = aoc.parse_multi_str_per_line
    # INPUT_PARSER = aoc.parse_one_int
    # INPUT_PARSER = aoc.parse_one_int_per_line
    INPUT_PARSER = aoc.parse_ints_per_line
    # INPUT_PARSER = aoc.parse_re_group_str(r"(a) .* (b) .* (c)")
    # INPUT_PARSER = aoc.parse_re_findall_str(r"(a|b|c)")
    # INPUT_PARSER = aoc.parse_multi_mixed_per_line
    # INPUT_PARSER = aoc.parse_re_group_mixed(r"(foo) .* (\d+)")
    # INPUT_PARSER = aoc.parse_re_findall_mixed(r"\d+|foo|bar")
    # INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_re_findall_int(r"\d+")])
    # INPUT_PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
    # INPUT_PARSER = aoc.AsciiBoolMapParser("#")
    # INPUT_PARSER = aoc.char_map
    # ---
    # INPUT_PARSER = aoc.CharCoordinatesParser("S.#")
    # (width, height), start, garden, rocks = puzzle_input
    # max_x, max_y = width - 1, height - 1

    def valid(self, result, rest, op_three):
        if len(rest) == 1:
            return result == rest[0]
        return (
            self.valid(result, [rest[0] + rest[1]] + rest[2:], op_three)
            or self.valid(result, [rest[0] * rest[1]] + rest[2:], op_three) 
            or (op_three and self.valid(result, [int(str(rest[0]) + str(rest[1]))] + rest[2:], op_three))
        )

    def part1(self, puzzle_input: InputType) -> int:
        total = 0
        for result, *rest in puzzle_input:
            if self.valid(result, rest, False):
                total += result

        return total

    def part2(self, puzzle_input: InputType) -> int:
        total = 0
        for result, *rest in puzzle_input:
            if self.valid(result, rest, True):
                total += result

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
