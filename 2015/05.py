#!/bin/python
"""Advent of Code: Day 05."""

import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = """\
ugknbfddgicrmopn
aaa
jchzalrnumimnmhp
haegwjzuvuyypxyu
dvszwmarrgswjxmb
qjhvhtzxzqqjkmpb
xxyxx
uurcxstgmygtbstg
ieodomkazucvgmuy""".splitlines()

InputType = list[int]
VOWELS = set("aeiou")
BAD = {"ab", "cd", "pq", "xy"}


class Day05(aoc.Challenge):
    """Day 5: Doesn't He Have Intern-Elves For This?."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=1),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=1),
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=0),
        aoc.TestCase(inputs=SAMPLE[3], part=1, want=0),
        aoc.TestCase(inputs=SAMPLE[4], part=1, want=0),
        aoc.TestCase(inputs=SAMPLE[5], part=2, want=1),
        aoc.TestCase(inputs=SAMPLE[6], part=2, want=1),
        aoc.TestCase(inputs=SAMPLE[7], part=2, want=0),
        aoc.TestCase(inputs=SAMPLE[8], part=2, want=0),
    )

    # Convert lines to type:
    INPUT_TYPES = str
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        total = 0
        for line in parsed_input:
            vowels = sum(True for i in line if i in VOWELS)
            if vowels < 3:
                continue
            if any(b in line for b in BAD):
                continue
            if all(a != b for a, b in zip(line, line[1:])):
                continue
            total += 1
        return total
        
    def part2(self, parsed_input: InputType) -> int:
        total = 0
        for line in parsed_input:
            repeated = False
            doubled = False
            for i in range(len(line) - 2):
                if not repeated and line[i:i + 2] in line[i + 2:]:
                    repeated = True
                if not doubled and line[i] == line[i+2]:
                    doubled = True
                if repeated and doubled:
                    total += 1
                    break
        return total

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().parse_input(puzzle_input)

        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]

        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]


if __name__ == "__main__":
    typer.run(Day05().run)

# vim:expandtab:sw=4:ts=4
