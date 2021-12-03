#!/bin/python

"""Advent of Code: Day 03."""

import collections
import functools
import math
import re
import typer
from typing import Any, Callable

from lib import aoc

SAMPLE = ["""\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""]


class Day03(aoc.Challenge):

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=198),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=230),
    )

    # Convert lines to type:
    INPUT_TYPES = str
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part2(self, lines: list[str]) -> int:
        most = ""
        least = ""
        
        all_lines = lines.copy()
        for i in range(len(lines[0])):

            c = collections.Counter(l[i] for l in all_lines)
            if c["1"] >= c["0"]:
                want = "1"
            else:
                want = "0"

            all_lines = [l for l in all_lines if l[i] == want]
            if len(all_lines) == 1:
                break

        ll_lines = lines.copy()
        for i in range(len(lines[0])):
            c = collections.Counter(l[i] for l in ll_lines)
            if c["1"] >= c["0"]:
                want = "0"
            else:
                want = "1"

            ll_lines = [l for l in ll_lines if l[i] == want]
            if len(ll_lines) == 1:
                break

        print(all_lines)
        print(ll_lines)
        return int(all_lines[0], base=2) * int(ll_lines[0], base=2)


    def part1(self, lines: list[str]) -> int:
        most = ""
        least = ""
        for i in range(len(lines[0])):
            c = collections.Counter(l[i] for l in lines)
            if c["1"] > c["0"]:
                most += "1"
                least += "0"
            else:
                most += "0"
                least += "1"
        return int(most, base=2) * int(least, base=2)

    def parse_input(self, puzzle_input: str):
        """Parse the input data."""
        return super().parse_input(puzzle_input)

        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]

        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]


if __name__ == '__main__':
    typer.run(Day03().run)

