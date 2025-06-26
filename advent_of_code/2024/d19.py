#!/bin/python
"""Advent of Code, Day 19: Linen Layout."""

import functools
from lib import aoc

SAMPLE = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""


class Day19(aoc.Challenge):
    """Day 19: Linen Layout."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=6),
        aoc.TestCase(part=2, inputs=SAMPLE, want=16),
    ]
    INPUT_PARSER = aoc.ParseBlocks([
        aoc.ParseMultiWords(input_type=str, separator=", "),
        aoc.parse_one_str_per_line,
    ])

    # This method is faster for p1 but it is nice similar code can solve both parts.
    def part1_fast(self, puzzle_input: tuple[list[str], list[str]]) -> int:
        """Return how many patterns can be formed with the given towels."""
        towels, patterns = puzzle_input
        towels.sort(key=len)

        @functools.cache
        def possible(pattern: str) -> bool:
            return any(
                pattern == towel or (
                    pattern.startswith(towel) and possible(pattern.removeprefix(towel))
                )
                for towel in towels
            )

        return sum(1 for pattern in patterns if possible(pattern))

    def solver(self, puzzle_input: tuple[list[str], list[str]], part_one: bool) -> int:
        """Return how many ways the patterns can be formed with the given towels."""
        towels, patterns = puzzle_input

        @functools.cache
        def possible(pattern: str) -> int:
            count = 0
            for towel in towels:
                if pattern == towel:
                    count += 1
                elif pattern.startswith(towel):
                    count += possible(pattern.removeprefix(towel))
            return count

        if part_one:
            return sum(1 for pattern in patterns if possible(pattern))
        return sum(possible(pattern) for pattern in patterns)

# vim:expandtab:sw=4:ts=4
