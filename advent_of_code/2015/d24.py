#!/bin/python
"""Advent of Code, Day 24: It Hangs in the Balance. Balance numbers into groups with contraints."""

import itertools
import math

from lib import aoc

SAMPLE = "\n".join([str(i) for i in list(range(1, 6)) + list(range(7, 12))])


def balance(packages: list[int], groups: int) -> int:
    """Return the group of packages which meets the constraints."""
    group_size = sum(packages) // groups
    candidates = []
    for package_count in range(1, len(packages)):
        for group in itertools.combinations(packages, package_count):
            if sum(group) == group_size:
                candidates.append(math.prod(group))
        if candidates:
            break
    return min(candidates)


def solve(data: list[int], part: int) -> int:
    """Return the smallest group, with 3/4 groups."""
    return balance(data, 3 if part == 1 else 4)


TESTS = [(1, SAMPLE, 99), (2, SAMPLE, 44)]
