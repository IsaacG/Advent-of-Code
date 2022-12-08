#!/bin/python
"""Advent of Code, Day 16: Aunt Sue."""

import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = [
    'children',  # 0
    'cats',  # 1
    'goldfish',  # 2
    'trees',  # 3
    'cars',  # 4
    'perfumes',  # 5
    """\
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1""",  # 6
]

LineType = int
InputType = list[LineType]
WANT = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


class Day16(aoc.Challenge):
    """Day 16: Aunt Sue."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=0),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=0),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        for i, aunt in enumerate(parsed_input):
            if all(WANT[k] == v for k, v in aunt.items()):
                return i + 1

    def part2(self, parsed_input: InputType) -> int:
        comp = {
            "children": lambda x: x == 3,
            "cats": lambda x: x > 7,
            "samoyeds": lambda x: x == 2,
            "pomeranians": lambda x: x < 3,
            "akitas": lambda x: x == 0,
            "vizslas": lambda x: x == 0,
            "goldfish": lambda x: x < 5,
            "trees": lambda x: x > 3,
            "cars": lambda x: x == 2,
            "perfumes": lambda x: x == 1,
        }
        for i, aunt in enumerate(parsed_input):
            if all(comp[k](v) for k, v in aunt.items()):
                return i + 1

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [
            dict(
                (prop.split(": ")[0], int(prop.split(": ")[1]))
                for prop in line.split(": ", 1)[1].split(", ")
            )
            for line in puzzle_input.splitlines()
        ]



if __name__ == "__main__":
    typer.run(Day16().run)

# vim:expandtab:sw=4:ts=4
