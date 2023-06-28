#!/bin/python
"""Advent of Code, Day 8: Two-Factor Authentication."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = """\
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1"""

LineType = int
InputType = list[LineType]


class Day08(aoc.Challenge):
    """Day 8: Two-Factor Authentication."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=6),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_one_str_per_line

    def part1(self, parsed_input: InputType) -> int:
        width, height = (7, 3) if self.testing else (50, 6)
        grid = [[False] * width for _ in range(height)]

        nums = re.compile(r"\d+")
        for num, line in enumerate(parsed_input):
            a, b = (int(i) for i in nums.findall(line))
            if line.startswith("rect"):
                for y in range(b):
                    for x in range(a):
                        grid[y][x] = True
            elif line.startswith("rotate row"):
                b %= width
                grid[a] = grid[a][-b:] + grid[a][:-b]
            elif line.startswith("rotate column"):
                b %= height
                col = [row[a] for row in grid]
                for y in range(height):
                    grid[y][a] = col[(y - b + height) % height]
            else:
                print("Not found")

            if self.testing:
                print(line)
                aoc.OCR(grid, validate=False).render()
        count = sum(i for row in grid for i in row)
        if not self.testing: assert count != 97
        return count

    def part2(self, parsed_input: InputType) -> int:
        width, height = (7, 3) if self.testing else (50, 6)
        grid = [[False] * width for _ in range(height)]

        nums = re.compile(r"\d+")
        for num, line in enumerate(parsed_input):
            a, b = (int(i) for i in nums.findall(line))
            if line.startswith("rect"):
                for y in range(b):
                    for x in range(a):
                        grid[y][x] = True
            elif line.startswith("rotate row"):
                b %= width
                grid[a] = grid[a][-b:] + grid[a][:-b]
            elif line.startswith("rotate column"):
                b %= height
                col = [row[a] for row in grid]
                for y in range(height):
                    grid[y][a] = col[(y - b + height) % height]
            else:
                print("Not found")

        res = aoc.OCR(grid).as_string()
        assert "?" not in res, res
        return res


    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

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
