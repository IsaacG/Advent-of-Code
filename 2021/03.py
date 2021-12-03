#!/bin/python

"""Advent of Code: Day 03."""

import collections
import functools
import math
import re
import typer
from typing import Any, Callable

from lib import aoc

SAMPLE = ["""\
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
"""]


class Day03(aoc.Challenge):

    """Submarine Diagnostics Analysis."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=198),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=230),
    )

    INPUT_TYPES = str

    def common(self, lines: list[str], position: int) -> tuple[str, str]:
        """Return the most and least common values found at a given position."""
        count = collections.Counter(l[position] for l in lines)
        if count["1"] >= count["0"]:
            return ("1", "0")
        else:
            return ("0", "1")

    def part1(self, lines: list[str]) -> int:
        """Find the most and least common value across all numbers."""
        most = "".join(self.common(lines, i)[0] for i in range(len(lines[0])))
        least = "".join(self.common(lines, i)[1] for i in range(len(lines[0])))
        return int(most, base=2) * int(least, base=2)

    def part2(self, lines: list[str]) -> int:
        """Use the most/least common values to filter the numbers there is just one."""
        nums = lines.copy()
        for i in range(len(lines[0])):
            want = self.common(nums, i)[0]
            nums = [l for l in nums if l[i] == want]
            if len(nums) == 1:
                num_one = nums[0]
                break

        nums = lines.copy()
        for i in range(len(lines[0])):
            want = self.common(nums, i)[1]
            nums = [l for l in nums if l[i] == want]
            if len(nums) == 1:
                num_two = nums[0]
                break

        return int(num_one, base=2) * int(num_two, base=2)


if __name__ == '__main__':
    typer.run(Day03().run)

