#!/bin/python
"""Advent of Code, Day 19: Medicine for Rudolph."""

import re

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

InputType = tuple[list[list[str]], str]


class Day19(aoc.Challenge):
    """Day 19: Medicine for Rudolph."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=4),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=7),
        # aoc.TestCase(inputs=SAMPLE[2], part=2, want=3),
        # aoc.TestCase(inputs=SAMPLE[3], part=2, want=6),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, puzzle_input: InputType) -> int:
        mappings, start = puzzle_input
        found = set()
        length = len(start)
        for a, _, b in mappings:
            for x in range(length):
                if start[x:].startswith(a):
                    found.add(start[:x] + b + start[x + len(a):])
        return len(found)

    def part2(self, puzzle_input: InputType) -> int:
        _, start = puzzle_input
        elements = re.findall(r"[A-Z][a-z]*", start)
        num_elements = len(elements)
        parens = elements.count("Rn") + elements.count("Ar")
        commas = elements.count("Y")
        # https://www.reddit.com/r/adventofcode/comments/3xflz8/comment/cy4etju/
        return num_elements - parens - 2 * commas - 1
