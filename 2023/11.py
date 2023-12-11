#!/bin/python
"""Advent of Code, Day 11: Cosmic Expansion."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""",  # 2
]

LineType = int
InputType = list[LineType]


class Day11(aoc.Challenge):
    """Day 11: Cosmic Expansion."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=374),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
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

    def solve_with(self, data: InputType, distance: int) -> int:
        data = data.copy()
        distance -= 1
        min_x, min_y, max_x, max_y = aoc.bounding_coords(data)

        offset_rows, offset_columns = [], []

        offset = complex(0)
        for x in range(min_x, max_x + 1):
            if not any(pos.real == x for pos in data):
                offset += complex(distance)
            offset_columns.append(offset)

        offset = complex(0)
        for y in range(min_y, max_y + 1):
            if not any(pos.imag == y for pos in data):
                offset += complex(0, distance)
            offset_rows.append(offset)

        data = {
            pos + offset_columns[int(pos.real)] + offset_rows[int(pos.imag)]
            for pos in data
        }

        return int(
            sum(
                abs(a.real - b.real) + abs(a.imag - b.imag)
                for a, b in itertools.combinations(data, 2)
            )
        )

    def part1(self, parsed_input: InputType) -> int:
        return self.solve_with(parsed_input.copy(), 2)

    def part2(self, parsed_input: InputType) -> int:
        d = 1000000
        result = self.solve_with(parsed_input.copy(), d)
        assert result < 731244992588
        return result

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        parser = aoc.parse_ascii_bool_map("#")
        return  parser.parse(puzzle_input)

# vim:expandtab:sw=4:ts=4
