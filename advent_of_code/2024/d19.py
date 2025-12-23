#!/bin/python
"""Advent of Code, Day 19: Linen Layout."""

import functools
from lib import aoc
PARSER = aoc.ParseBlocks([
    aoc.ParseMultiWords(input_type=str, separator=", "),
    aoc.parse_one_str_per_line,
])


# This method is faster for p1 but it is nice similar code can solve both parts.
def part1_fast(data: tuple[list[str], list[str]]) -> int:
    """Return how many patterns can be formed with the given towels."""
    towels, patterns = data
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


def solve(data: tuple[list[str], list[str]], part: int) -> int:
    """Return how many ways the patterns can be formed with the given towels."""
    towels, patterns = data

    @functools.cache
    def possible(pattern: str) -> int:
        count = 0
        for towel in towels:
            if pattern == towel:
                count += 1
            elif pattern.startswith(towel):
                count += possible(pattern.removeprefix(towel))
        return count

    if part == 1:
        return sum(1 for pattern in patterns if possible(pattern))
    return sum(possible(pattern) for pattern in patterns)


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
TESTS = [(1, SAMPLE, 6), (2, SAMPLE, 16)]
# vim:expandtab:sw=4:ts=4
