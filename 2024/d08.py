#!/bin/python
"""Advent of Code, Title."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

LineType = int
InputType = list[LineType]


class Day08(aoc.Challenge):
    """Title."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=14),
        aoc.TestCase(part=2, inputs=SAMPLE, want=34),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    def part1(self, puzzle_input: InputType) -> int:
        size = puzzle_input[0]
        antinodes = set()
        all_locations = set().union(*puzzle_input[1].values())
        for freq, coords in puzzle_input[1].items():
            if freq == ".":
                continue
            f_nodes = set()
            for a, b in itertools.combinations(coords, 2):
                f_nodes.add(b + (b - a))
                f_nodes.add(a + (a - b))
            f_nodes &= all_locations
            antinodes |= f_nodes

        # aoc.print_point_set(antinodes)
        return len(antinodes)

    def part2(self, puzzle_input: InputType) -> int:
        antinodes = set()
        all_locations = set().union(*puzzle_input[1].values())
        for freq, coords in puzzle_input[1].items():
            if freq == ".":
                continue
            for a, b in itertools.combinations(coords, 2):
                delta = a - b
                for i in itertools.count():
                    if a + i * delta in all_locations:
                        antinodes.add(a + i * delta)
                    else:
                        break

                for i in itertools.count():
                    if a - i * delta in all_locations:
                        antinodes.add(a - i * delta)
                    else:
                        break

        # aoc.print_point_set(antinodes)
        return len(antinodes)

    # def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        lines = puzzle_input.splitlines()
        size = (len(lines[0]), len(lines))
        data = collections.defaultdict(set)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                data[char].add(complex(x, y))
        return size, dict(data)

# vim:expandtab:sw=4:ts=4
