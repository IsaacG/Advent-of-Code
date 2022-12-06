#!/bin/python
"""Advent of Code: Day 06."""

import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = ["bvwbjplbgvbhsrlpgdmjqwftvncz", "nppdvjthqldpwncqszvftbrmjlhg", "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
          "mjqjpqmgbljsphdztnvjfqwrcgsmlb"]

LineType = int
InputType = list[LineType]


class Day06(aoc.Challenge):
    """Day 6: Tuning Trouble."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=5),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=6),
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=10),
        aoc.TestCase(inputs=SAMPLE[3], part=1, want=11),
        aoc.TestCase(inputs=SAMPLE[4], part=2, want=19),
    ]

    # Convert lines to type:
    INPUT_TYPES = LineType
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        g = zip(parsed_input, parsed_input[1:], parsed_input[2:], parsed_input[3:])
        for i, (a, b, c, d) in enumerate(g):
            if len(set([a, b, c, d])) == 4:
                return i + 4

    def part2(self, parsed_input: InputType) -> int:
        parts = [parsed_input[i:] for i in range(14)]
        g = zip(*parts)
        for i, (x) in enumerate(g):
            if len(set(x)) == 14:
                return i + 14


    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return puzzle_input
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]

    # def line_parser(self, line: str) -> LineType:
    #     """If defined, use this to parse single lines."""
    #     return (
    #         int(i) if i.isdigit() else i
    #         for i in PARSE_RE.findall(line)
    #     )


if __name__ == "__main__":
    typer.run(Day06().run)

# vim:expandtab:sw=4:ts=4
