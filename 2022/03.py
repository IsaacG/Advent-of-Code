#!/bin/python
"""Advent of Code: Day 03."""

import collections
import functools
import more_itertools
import string
import math
import re

import typer
from lib import aoc

SAMPLE = ["""\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""]
InputType = list[str]


class Day03(aoc.Challenge):

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=157),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=70),
    )

    # Convert lines to type:
    INPUT_TYPES = str
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        s = string.ascii_lowercase + string.ascii_uppercase
        score = 0
        for line in parsed_input:
            a, b = line[:len(line) // 2], line[len(line)//2:]
            common = list(set(a) & set(b))
            assert len(common) == 1
            score += s.index(common[0]) + 1

        return score

    def part2(self, parsed_input: InputType) -> int:
        s = string.ascii_lowercase + string.ascii_uppercase
        score = 0
        for lines in more_itertools.chunked(parsed_input, 3):
            common = list(set(lines[0]) & set(lines[1]) & set(lines[2]))
            assert len(common) == 1
            score += s.index(common[0]) + 1

        return score

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().parse_input(puzzle_input)

        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]

        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]


if __name__ == "__main__":
    typer.run(Day03().run)

# vim:expandtab:sw=4:ts=4
