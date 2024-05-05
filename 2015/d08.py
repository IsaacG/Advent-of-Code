#!/bin/python
"""Advent of Code: Day 08."""

from lib import aoc

SAMPLE = [
    '""',
    '"abc"',
    r'"aaa\"aaa"',
    r'"\x27"',
]

LineType = str
InputType = list[LineType]


class Day08(aoc.Challenge):
    """Day 8: Matchsticks. Escape and un-escape strings."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=2),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=2),
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=3),
        aoc.TestCase(inputs=SAMPLE[3], part=1, want=5),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=4),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=4),
        aoc.TestCase(inputs=SAMPLE[2], part=2, want=6),
        aoc.TestCase(inputs=SAMPLE[3], part=2, want=5),
    ]

    def part1(self, parsed_input: InputType) -> int:
        """Return the length of escaping chars compared to decoded version."""
        return sum(
            len(a) - len(eval(a))
            for a in parsed_input
        )

    def part2(self, parsed_input: InputType) -> int:
        """Return the length of escaping chars compared to encoded version."""
        return sum(
            2 + a.count('"') + a.count("\\")
            for a in parsed_input
        )
