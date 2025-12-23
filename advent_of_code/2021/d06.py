#!/bin/python
"""Advent of Code: Day 06. Compute how many lantern fish there are, after they breed."""

import collections


def solve(data: list[int], part: int) -> int:
    """Compute fish population after N days."""
    days = 80 if part == 1 else 256
    # Construct the initial population map. Age -> count.
    counter = dict(collections.Counter(data))
    for _ in range(days):
        # Reduce day counter for all fish.
        new = {k - 1: v for k, v in counter.items() if k}
        # Add new baby fish and reset the counter on fish that spawned.
        new[6] = counter.get(0, 0) + counter.get(7, 0)
        new[8] = counter.get(0, 0)
        counter = new
    return sum(counter.values())


SAMPLE = "3,4,3,1,2"
TESTS = [(1, SAMPLE, 5934), (2, SAMPLE, 26984457539)]
