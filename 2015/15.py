#!/bin/python
"""Advent of Code, Day 15: Science for Hungry People."""

import itertools
import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = """\
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""

LineType = int
InputType = list[LineType]


class Day15(aoc.Challenge):
    """Day 15: Science for Hungry People."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=62842880),
        aoc.TestCase(inputs=SAMPLE, part=2, want=57600000),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        use = "capacity durability flavor texture".split()
        most = 0
        n = len(parsed_input)
        for amounts in itertools.permutations(range(101), n - 1):
            amounts += (100 - sum(amounts),)
            total = 1
            for prop in use:
                total *= max(0, sum(
                    m * d[prop]
                    for m, d in zip(amounts, parsed_input)
                ))
            if total > most:
                most = total
        return most

    def part2(self, parsed_input: InputType) -> int:
        use = "capacity durability flavor texture".split()
        calories = 500
        most = 0
        n = len(parsed_input)
        for amounts in itertools.permutations(range(101), n - 1):
            amounts += (100 - sum(amounts),)
            if sum(
                m * d["calories"]
                for m, d in zip(amounts, parsed_input)
            ) != 500:
                continue
            total = 1
            for prop in use:
                total *= max(0, sum(
                    m * d[prop]
                    for m, d in zip(amounts, parsed_input)
                ))
            if total > most:
                most = total
        return most


    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        data = []
        for line in puzzle_input.splitlines():
            name, properties = line.split(": ", 1)
            data.append({
                prop.split()[0]: int(prop.split()[-1])
                for prop in properties.split(", ")
            })
        return data

if __name__ == "__main__":
    typer.run(Day15().run)

# vim:expandtab:sw=4:ts=4
