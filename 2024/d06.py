#!/bin/python
"""Advent of Code, Title."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

LineType = int
InputType = list[LineType]


class Day06(aoc.Challenge):
    """Title."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=41),
        aoc.TestCase(part=2, inputs=SAMPLE, want=6),
    ]

    INPUT_PARSER = aoc.CharCoordParser()

    def walk(self, all_spots, blocked, pos, direction):
        spots = set()
        seen = set()
        while pos in all_spots:
            spots.add(pos)
            if (pos, direction) in seen:
                break
            seen.add((pos, direction))
            while pos + direction in blocked:
                direction *= 1j
            pos += direction
        return spots, (pos, direction) in seen

    def part1(self, puzzle_input: InputType) -> int:
        all_spots, blocked, start_pos, start_dir = puzzle_input
        spots, is_loop = self.walk(all_spots, blocked, start_pos, start_dir)
        return len(spots)

    def part2(self, puzzle_input: InputType) -> int:
        all_spots, blocked, start_pos, start_dir = puzzle_input

        spots, is_loop = self.walk(all_spots, blocked, start_pos, start_dir)
        spots.remove(start_pos)

        found = set()
        for option in spots:
            _, is_loop = self.walk(all_spots, blocked | {option}, start_pos, start_dir)
            if is_loop:
                found.add(option)

        count = len(found)
        return count

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        lines = puzzle_input.splitlines()
        all_spots = set()
        blocked = set()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                all_spots.add(complex(x, y))
                if char == "#":
                    blocked.add(complex(x, y))
                if char in "<>v^":
                    start_pos = complex(x, y)
                    start_dir = aoc.ARROW_DIRECTIONS[char]
        return all_spots, blocked, start_pos, start_dir

# vim:expandtab:sw=4:ts=4
