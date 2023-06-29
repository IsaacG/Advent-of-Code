#!/bin/python
"""Advent of Code: Day 03."""

import string
import more_itertools

import typer
from lib import aoc

SAMPLE = ["""\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""]
InputType = list[str]

SCORING = " " + string.ascii_letters


class Day03(aoc.Challenge):
    """Day 3: Rucksack Reorganization. Find common elements across groupings."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=157),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=70),
    ]

    def part1(self, parsed_input: InputType) -> int:
        """Find the common element across the first and second half of each line."""
        score = 0
        for line in parsed_input:
            middle = len(line) // 2
            a, b = line[:middle], line[middle:]
            common = set(a) & set(b)
            assert len(common) == 1
            score += SCORING.index(common.pop())

        return score

    def part2(self, parsed_input: InputType) -> int:
        """Find the common element across groups of three lines."""
        score = 0
        for lines in more_itertools.chunked(parsed_input, 3):
            common = set(lines[0]) & set(lines[1]) & set(lines[2])
            assert len(common) == 1
            score += SCORING.index(common.pop())

        return score


if __name__ == "__main__":
    typer.run(Day03().run)

# vim:expandtab:sw=4:ts=4
