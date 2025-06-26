#!/bin/python
"""Advent of Code, Day 4: High-Entropy Passphrases."""

import itertools
from lib import aoc

SAMPLE = [
    """\
aa bb cc dd ee
aa bb cc dd aa
aa bb cc dd aaa""",
    """\
abcde fghij
abcde xyz ecdab
a ab abc abd abf abj
iiii oiii ooii oooi oooo
oiii ioii iioi iiio"""
]


class Day04(aoc.Challenge):
    """Day 4: High-Entropy Passphrases. Count valid passphrases."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=2),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=3),
    ]

    def part1(self, puzzle_input: list[list[str]]) -> int:
        """Count passphrases where no word is repeated."""
        return sum(len(set(line)) == len(line) for line in puzzle_input)

    def part2(self, puzzle_input: list[list[str]]) -> int:
        """Count passphrases where no word is an anagram of another."""
        return sum(
            all(sorted(a) != sorted(b) for a, b in itertools.combinations(line, 2))
            for line in puzzle_input
        )

# vim:expandtab:sw=4:ts=4
