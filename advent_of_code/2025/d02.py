#!/bin/python
"""Advent of Code, Day 2: Gift Shop."""

import re
from lib import aoc

SAMPLE = (
    "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,"
    + "446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
)


class Day02(aoc.Challenge):
    """Day 2: Gift Shop."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=1227775554),
        aoc.TestCase(part=2, inputs=SAMPLE, want=4174379265),
    ]
    INPUT_PARSER = aoc.parse_re_findall_int(r"\d+")

    def solver(self, puzzle_input: list[list[int]], part_one: bool) -> int:
        """Find all repeated digits in ranges."""
        pattern = re.compile(r"(\d+)\1" if part_one else r"(\d+)\1+")
        return sum(
            digit
            for start, end in zip(puzzle_input[0][::2], puzzle_input[0][1::2])
            for digit in range(start, end + 1)
            if pattern.fullmatch(str(digit))
        )

# vim:expandtab:sw=4:ts=4
