#!/bin/python
"""Advent of Code, Day 10: Hoof It."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
9990999
9991999
9992999
6543456
7111117
8111118
9111119""",
    """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""",  # 18
]

LineType = int
InputType = list[LineType]


class Day10(aoc.Challenge):
    """Day 10: Hoof It."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=2),
        aoc.TestCase(part=1, inputs=SAMPLE[1], want=36),
        aoc.TestCase(part=2, inputs=SAMPLE[1], want=81),
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
    # INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_re_findall_int(r"\d+")])
    # INPUT_PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
    INPUT_PARSER = aoc.CoordinatesParser(chars=None, origin_top_left=True)

    def part2(self, puzzle_input: InputType) -> int:
        total = 0
        for trailhead in puzzle_input[0]:
            paths = {(trailhead, (trailhead,))}
            for i in range(1, 10):
                next_paths = set()
                for last, path in paths:
                    coords = puzzle_input[i]
                    for neighbor in aoc.FOUR_DIRECTIONS:
                        if (new_pos := last + neighbor) in coords:
                            next_paths.add((new_pos, path + (new_pos,)))
                paths = next_paths
            total += len(paths)
        return total


        print("\n".join(["==="] + [f"{k}={v!r}" for k, v in locals().items()] + ["==="]))
        return None

    def part1(self, puzzle_input: InputType) -> int:
        total = 0
        for trailhead in puzzle_input[0]:
            paths = {trailhead}
            for i in range(1, 10):
                next_paths = set()
                for last in paths:
                    coords = puzzle_input[i]
                    for neighbor in aoc.FOUR_DIRECTIONS:
                        if (new_pos := last + neighbor) in coords:
                            next_paths.add(new_pos)
                paths = next_paths
            self.tprint(f"{trailhead=} -> {len(paths)}")
            total += len(paths)
        return total

    # def part2(self, puzzle_input: InputType) -> int:

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
