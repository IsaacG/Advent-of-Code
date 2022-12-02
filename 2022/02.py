#!/bin/python
"""Advent of Code: Day 02."""

import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = ["""\
A Y
B X
C Z
"""]
InputType = list[int]


class Day02(aoc.Challenge):

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=15),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=12),
    )

    # Convert lines to type:
    INPUT_TYPES = int
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        score = 0
        for a, b in parsed_input:
            a1 = "ABC".index(a)
            b1 = "XYZ".index(b)
            score += b1 + 1
            if a1 == b1:
                score += 3 # draw
            if b1 == a1 + 1 or a1 == 2 and b1 == 0:
                score += 6 # win
        return score

    def part2(self, parsed_input: InputType) -> int:
        # X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!"
        score = 0
        for a, b in parsed_input:
            a1 = "ABC".index(a)
            if b == "X":
                score += {"A": 3, "B": 1, "C": 2}[a]
            if b == "Y":
                score += 3 # draw
                score += a1 + 1
            if b == "Z":
                score += 6 # win
                score += {"A": 2, "B": 3, "C": 1}[a]

        return score


    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [i.split() for i in puzzle_input.splitlines()]

        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]


if __name__ == "__main__":
    typer.run(Day02().run)

# vim:expandtab:sw=4:ts=4
