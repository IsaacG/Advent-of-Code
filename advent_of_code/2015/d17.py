#!/bin/python
"""Advent of Code, Day 17: No Such Thing as Too Much. Count ways to fill containers."""

import collections
import itertools


def count(containers: list[int], testing: bool) -> dict[int, int]:
    """Compute the number of ways to fill containers."""
    target = 25 if testing else 150
    counts: dict[int, int] = collections.defaultdict(int)
    for number in range(len(containers)):
        for combo in itertools.combinations(containers, number):
            if sum(combo) == target:
                counts[number] += 1
    return counts


def solve(data: list[int], part: int, testing: bool) -> int:
    """Return the possible countainer combos which fit the eggnog or minimizes containers."""
    counts = count(data, testing)
    if part == 1:
        return sum(counts.values())
    return counts[min(counts)]


SAMPLE = """\
20
15
10
5
5"""
TESTS = [(1, SAMPLE, 4), (2, SAMPLE, 3)]
