#!/bin/python

"""Advent of Code: Day 03."""

import collections

from lib import aoc

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


class Day03(aoc.Challenge):
    """Submarine Diagnostics Analysis."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=198),
        aoc.TestCase(inputs=SAMPLE, part=2, want=230),
    )
    INPUT_PARSER = aoc.parse_one_str_per_line

    @staticmethod
    def common(puzzle_input: list[str], position: int) -> tuple[str, str]:
        """Return the most and least common values found at a given position."""
        count = collections.Counter(line[position] for line in puzzle_input)
        return ("1", "0") if count["1"] >= count["0"] else ("0", "1")

    def part1(self, puzzle_input: list[str]) -> int:
        """Find the most and least common value across all numbers."""
        result = 1
        for most_least in range(2):
            num = "".join(self.common(puzzle_input, i)[most_least] for i in range(len(puzzle_input[0])))
            result *= int(num, base=2)
        return result

    def part2(self, puzzle_input: list[str]) -> int:
        """Use the most/least common values to filter the numbers there is just one."""
        result = 1
        for most_least in range(2):
            nums = puzzle_input.copy()
            for i in range(len(puzzle_input[0])):
                want = self.common(nums, i)[most_least]
                nums = [num for num in nums if num[i] == want]
                if len(nums) == 1:
                    result *= int(nums[0], base=2)
                    break

        return result
