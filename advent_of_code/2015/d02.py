#!/bin/python
"""Advent of Code, Day 2: I Was Told There Would Be No Math. Compute wrapping materials."""
import itertools
import math


def solve(data: list[list[int]], part: int) -> int:
    """Return the amount of wrapping paper and ribbon needed."""
    total = 0
    for dims in data:
        if part == 1:
            sides = [a * b for a, b in itertools.combinations(dims, 2)]
            total += sum(sides) * 2 + min(sides)
        else:
            perimeters = [a + b for a, b in itertools.combinations(dims, 2)]
            total += min(perimeters) * 2 + math.prod(dims)
    return total


SAMPLE = ["2x3x4", "1x1x10"]
TESTS = [
    (1, SAMPLE[0], 58),
    (1, SAMPLE[1], 43),
    (2, SAMPLE[0], 34),
    (2, SAMPLE[1], 14),
]
