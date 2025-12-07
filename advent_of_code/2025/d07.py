#!/bin/python
"""Advent of Code, Day 7: Laboratories."""
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
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............""",  # 4
]

LineType = int
InputType = list[LineType]
log = logging.info


class Day07(aoc.Challenge):
    """Day 7: Laboratories."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=21),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=40),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    # INPUT_PARSER = aoc.parse_ints
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
    # INPUT_PARSER = aoc.CoordinatesParser(chars=None, origin_top_left=True)
    # ---
    # (width, height), start, garden, rocks = puzzle_input
    # max_x, max_y = width - 1, height - 1

    def part1(self, puzzle_input: InputType) -> int:
        start = puzzle_input.coords["S"].copy().pop()
        splitters = puzzle_input.coords["^"]
        beam, start_y = start
        beams = {beam,}
        split = 0
        for y in range(start_y, puzzle_input.height):
            todo = set()
            for beam in beams:
                if (beam, y) in splitters:
                    split += 1
                    todo.add(beam)
            beams = (beams - todo) | {i + 1 for i in todo} | {i - 1 for i in todo}
        return split

        return None

    def part2(self, puzzle_input: InputType) -> int:
        start = puzzle_input.coords["S"].copy().pop()
        splitters = puzzle_input.coords["^"]
        beam, start_y = start

        @functools.cache
        def timelines(beam, y):
            if y == puzzle_input.height:
                return 1
            y += 1
            if (beam, y) in splitters:
                return timelines(beam - 1, y) + timelines(beam + 1, y)
            return timelines(beam, y)

        return timelines(*start)
        beams = {beam,}
        split = 0
        for y in range(start_y, puzzle_input.height):
            todo = set()
            for beam in beams:
                if (beam, y) in splitters:
                    split += 1
                    todo.add(beam)
            beams = (beams - todo) | {i + 1 for i in todo} | {i - 1 for i in todo}
        return split


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
