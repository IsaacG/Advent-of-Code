#!/bin/python
"""Advent of Code: Day 03."""

import string
import more_itertools

from lib import aoc

SAMPLE = ["""\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""]
SCORING = " " + string.ascii_letters


class Day03(aoc.Challenge):
    """Day 3: Rucksack Reorganization. Find common elements across groupings."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=157),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=70),
    ]

    def part1(self, puzzle_input: list[str]) -> int:
        """Find the common element across the first and second half of each line."""
        score = 0
        for line in puzzle_input:
            middle = len(line) // 2
            a, b = line[:middle], line[middle:]
            common = set(a) & set(b)
            assert len(common) == 1
            score += SCORING.index(common.pop())

        return score

    def part2(self, puzzle_input: list[str]) -> int:
        """Find the common element across groups of three lines."""
        score = 0
        for lines in more_itertools.chunked(puzzle_input, 3):
            common = set(lines[0]) & set(lines[1]) & set(lines[2])
            assert len(common) == 1
            score += SCORING.index(common.pop())

        return score
