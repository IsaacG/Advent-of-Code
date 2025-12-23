#!/bin/python

"""Advent of Code: Day 03. Submarine Diagnostics Analysis."""

import collections
PARSER = str.splitlines


def common(data: list[str], position: int) -> tuple[str, str]:
    """Return the most and least common values found at a given position."""
    count = collections.Counter(line[position] for line in data)
    return ("1", "0") if count["1"] >= count["0"] else ("0", "1")


def solve(data: list[str], part: int) -> int:
    """Find the most and least common value across all numbers."""
    result = 1
    if part == 1:
        for most_least in range(2):
            num = "".join(common(data, i)[most_least] for i in range(len(data[0])))
            result *= int(num, base=2)
        return result
    for most_least in range(2):
        # Use the most/least common values to filter the numbers there is just one.
        nums = data.copy()
        for i in range(len(data[0])):
            want = common(nums, i)[most_least]
            nums = [num for num in nums if num[i] == want]
            if len(nums) == 1:
                result *= int(nums[0], base=2)
                break

    return result


SAMPLE = """\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""
TESTS = [(1, SAMPLE, 198), (2, SAMPLE, 230)]
