#!/bin/python
"""Advent of Code: Day 03.  Rucksack Reorganization. Find common elements across groupings."""

import string
import more_itertools

from lib import aoc
SCORING = " " + string.ascii_letters


def solve(data: list[str], part: int) -> int:
    """Solve the parts."""
    return (part1 if part == 1 else part2)(data)


def part1(data: list[str]) -> int:
    """Find the common element across the first and second half of each line."""
    score = 0
    for line in data:
        middle = len(line) // 2
        a, b = line[:middle], line[middle:]
        common = set(a) & set(b)
        score += SCORING.index(common.pop())

    return score

def part2(data: list[str]) -> int:
    """Find the common element across groups of three lines."""
    score = 0
    for lines in more_itertools.chunked(data, 3):
        common = set(lines[0]) & set(lines[1]) & set(lines[2])
        score += SCORING.index(common.pop())

    return score

SAMPLE = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""
TESTS = [(1, SAMPLE, 157), (2, SAMPLE, 70)]
