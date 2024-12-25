#!/bin/python
"""Advent of Code, Day 25: Code Chronicle."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####""",  # 0
]

LineType = int
InputType = list[LineType]


class Day25(aoc.Challenge):
    """Day 25: Code Chronicle."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=3),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    # INPUT_PARSER = aoc.parse_one_str
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
    # INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line])
    # INPUT_PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
    # INPUT_PARSER = aoc.CoordinatesParser(chars=None, origin_top_left=True)
    # ---
    # (width, height), start, garden, rocks = puzzle_input
    # max_x, max_y = width - 1, height - 1

    def part1(self, puzzle_input: InputType) -> int:
        keys, locks = puzzle_input
        return sum(
            1
            for k in keys
            for l in locks
            if all(a + b < 6 for a, b in zip(k, l))
        )
        return None

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        keys, locks = [], []
        for block in puzzle_input.split("\n\n"):
            kl = []
            for line in zip(*(block.splitlines())):
                want = 7
                assert len(line) == want, len(line)
                kl.append(line.count("#") - 1)
            if block[0] == "#":
                locks.append(kl)
            else:
                keys.append(kl)
        return keys, locks


                

# vim:expandtab:sw=4:ts=4
