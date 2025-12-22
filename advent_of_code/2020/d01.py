#!/usr/bin/env python
"""AoC Day 1: Report Repair."""


def prod_of_pair(pair_sum: int, data: list[int]) -> int:
    """Return the product of two values with a target sum."""
    vals = [i for i in data if pair_sum - i in data]
    if not vals:
        return 0
    if len(vals) == 2:
        return vals[0] * vals[1]
    raise ValueError('Found too many matches.')


def solve(data: list[int], part: int) -> int:
    """Compute products."""
    if part == 1:
        return prod_of_pair(2020, data)

    for n in data:
        subset = list(data)
        subset.remove(n)
        prod = prod_of_pair(2020 - n, subset)
        if prod:
            prod *= n
            return prod
    raise RuntimeError


SAMPLE = """\
1721
979
366
299
675
1456
"""
TESTS = [
  (1, SAMPLE, 514579),
  (2, SAMPLE, 241861950),
]
