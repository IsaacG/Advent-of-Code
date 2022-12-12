#!/bin/python
"""Advent of Code, Day 19: Medicine for Rudolph."""

import collections
import functools
import math
import queue
import re

import typer
from lib import aoc

SAMPLE = [
    """\
H => HO
H => OH
O => HH

HOH""",
    """\
H => HO
H => OH
O => HH

HOHOHO""", """\
e => H
e => O
H => HO
H => OH
O => HH

HOH""", """\
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO"""
]

LineType = int
InputType = list[LineType]


class Day19(aoc.Challenge):
    """Day 19: Medicine for Rudolph."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=4),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=7),
        aoc.TestCase(inputs=SAMPLE[2], part=2, want=3),
        aoc.TestCase(inputs=SAMPLE[3], part=2, want=6),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.ParseBlocks([aoc.parse_multi_str_per_line, aoc.parse_one_str])

    def part1(self, parsed_input: InputType) -> int:
        mappings, start = parsed_input
        found = set()
        length = len(start)
        for a, _, b in mappings:
            for x in range(length):
                if start[x:].startswith(a):
                    found.add(start[:x] + b + start[x + len(a):])
        return len(found)

    def part2(self, parsed_input: InputType) -> int:
        mappings, start = parsed_input
        for a, _, b in mappings:
            if len(a) > len(b):
                raise ValueError

        for step in range(1, 200000):
            if start == "e":
                return step
            for b, _, a in mappings:
                if a in start:
                    start = start.replace(a, b)
                    break
        raise RuntimeError

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

    # def line_parser(self, line: str):
    #     pass


if __name__ == "__main__":
    typer.run(Day19().run)

# vim:expandtab:sw=4:ts=4
