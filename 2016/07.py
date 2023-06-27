#!/bin/python
"""Advent of Code, Day 7: Internet Protocol Version 7. Detect line patterns."""

import re

from lib import aoc

SAMPLE = [
    """\
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn""",
    "aba[bab]xyz\naba[bab]xyz",
    "aba[bab]xyz\naaa[kek]eke",
    "aba[bab]xyz\nzazbz[bzb]cdb",
    "aba[bab]xyz\nxyx[xyx]xyx",
]

LineType = tuple[list[str], list[str]]
InputType = list[LineType]


class Day07(aoc.Challenge):
    """Day 7: Internet Protocol Version 7."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=2),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=2),
        aoc.TestCase(inputs=SAMPLE[2], part=2, want=2),
        aoc.TestCase(inputs=SAMPLE[3], part=2, want=2),
        aoc.TestCase(inputs=SAMPLE[4], part=2, want=1),
    ]

    def tls(self, string: str) -> bool:
        """Return if a string segment has a pattern ABBA."""
        return any(
            chars[0] == chars[3] and chars[1] == chars[2] and chars[0] != chars[1]
            for chars in zip(*[string[i:] for i in range(4)])
        )

    def ssl(self, outer: list[str], inner: list[str]) -> bool:
        """Return if inner and outer have a matching ABA, BAB."""
        patterns = [
            (chars[1] + chars[0] + chars[1])
            for chunk in inner
            for chars in zip(*[chunk[i:] for i in range(3)])
            if chars[0] == chars[2] != chars[1]
        ]
        return any(pattern in chunk for chunk in outer for pattern in patterns)

    def part1(self, parsed_input: InputType) -> int:
        """Return the number of lines with TLS patterns."""
        return sum(
            not any(self.tls(i) for i in inner)
            and any(self.tls(i) for i in outer)
            for outer, inner in parsed_input
        )

    def part2(self, parsed_input: InputType) -> int:
        """Return the number of lines with SSL patterns."""
        return sum(self.ssl(*line) for line in parsed_input)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        lines = []
        for line in puzzle_input.splitlines():
            parts = re.split(r"[][]", line)
            lines.append((parts[::2], parts[1::2]))
        return lines
