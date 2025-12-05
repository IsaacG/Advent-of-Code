#!/bin/python
"""Advent of Code, Day 5: Cafeteria."""
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
3-5
10-14
16-20
12-18

1
5
8
11
17
32""",  # 0
]

LineType = int
InputType = list[LineType]
log = logging.info


class Day05(aoc.Challenge):
    """Day 5: Cafeteria."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=3),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=14),
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
        a, b = puzzle_input.split("\n\n")
        # print("\n".join(["==="] + [f"{k}={v!r}" for k, v in locals().items()] + ["==="]))
        f = set()
        for l in a.splitlines():
            i, j = l.split("-")
            f.add((int(i), int(j)))

        t = 0
        for l in b.splitlines():
            i = int(l)
            if any(x <= i <= y for x, y in f):
                t += 1
        return t


    def part2(self, puzzle_input: InputType) -> int:
        a, b = puzzle_input.split("\n\n")
        # print("\n".join(["==="] + [f"{k}={v!r}" for k, v in locals().items()] + ["==="]))
        f = set()
        for l in a.splitlines():
            i, j = l.split("-")
            f.add((int(i), int(j)))

        total = 0
        f = sorted(f)
        opened, closed = f[0]
        for i in range(1, len(f)):
            if f[i][0] > closed:
                total += 1 + closed - opened
                opened, closed = f[i]
            else:
                closed = max(closed, f[i][1])
        total += 1 + closed - opened
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
