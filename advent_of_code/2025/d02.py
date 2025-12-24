#!/bin/python
"""Advent of Code, Day 2: Gift Shop."""

import re
from lib import aoc
PARSER = aoc.parse_re_findall_int(r"\d+")


def solve(data: list[list[int]], part: int) -> int:
    """Find all repeated digits in ranges."""
    pattern = re.compile(r"(\d+)\1" if part == 1 else r"(\d+)\1+")
    return sum(
        digit
        for start, end in zip(data[0][::2], data[0][1::2])
        for digit in range(start, end + 1)
        if pattern.fullmatch(str(digit))
    )


SAMPLE = (
    "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,"
    + "446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
)
TESTS = [
    (1, SAMPLE, 1227775554),
    (2, SAMPLE, 4174379265),
]
# vim:expandtab:sw=4:ts=4
