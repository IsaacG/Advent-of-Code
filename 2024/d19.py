#!/bin/python
"""Advent of Code, Day 19: Linen Layout."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb""",  # 12
    """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bbrgwb""",  # 12
]

LineType = int
InputType = list[LineType]


class Day19(aoc.Challenge):
    """Day 19: Linen Layout."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=6),
        aoc.TestCase(part=2, inputs=SAMPLE[1], want=2),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=16),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
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
    INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str, aoc.parse_one_str_per_line])

    def part1(self, puzzle_input: InputType) -> int:
        one, two = puzzle_input
        towels = sorted(one.split(", "), key=lambda x: len(x))
        
        @functools.cache
        def possible(pattern) -> bool:
            for towel in towels:
                if pattern == towel:
                    return True
                elif pattern.startswith(towel) and possible(pattern.removeprefix(towel)):
                    return True
                elif pattern.endswith(towel) and possible(pattern.removesuffix(towel)):
                    return True
            return False

        count = 0
        for patt in two:
            # print(f"check {patt}")
            if possible(patt):
                # print(f"{patt} possible")
                count += 1
            # else:
                # print(f"{patt} not possible")
        return count


    def part2(self, puzzle_input: InputType) -> int:
        one, two = puzzle_input
        towels = sorted(set(one.split(", ")), key=lambda x: len(x))

        @functools.cache
        def possible(pattern) -> bool:
            counts = 0
            # print(f"Solve {pattern}")
            for towel in towels:
                # print(f"Solve {pattern} --> using {towel}")
                n = 0
                if pattern == towel:
                    n += 1
                elif pattern.startswith(towel):
                    n += possible(pattern.removeprefix(towel))
                # print(f"Solve {pattern} --> using {towel} --> {n} ways")
                counts += n
            # print(f"{pattern} {counts}")
            return counts

        c = 0
        for patt in two:
            n = possible(patt)
            # print(f"{patt} {n}")
            c += n
        return c


# vim:expandtab:sw=4:ts=4
