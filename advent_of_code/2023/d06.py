#!/bin/python
"""Advent of Code, Day 6: Wait For It."""
import math
from lib import aoc
PARSER = aoc.parse_ints


def solve(data: list[list[int]], part: int) -> int:
    """Compute how long to charge the car in order to win the race."""
    if part == 1:
        times, distances = data
    else:
        times, distances = ([int("".join(str(i) for i in line))] for line in data)

    # See notes for explanation.
    result = 1
    for time, distance in zip(times, distances):
        common = math.sqrt(time**2 - 4 * distance) / 2
        x1_exact = time / 2 - common
        x2_exact = time / 2 + common
        x1 = math.ceil(x1_exact)
        x2 = math.floor(x2_exact)
        if x1 == x1_exact:
            x1 += 1
        if x2 == x2_exact:
            x2 -= 1
        result *= (x2 - x1 + 1)
    return result


SAMPLE = """\
Time:      7  15   30
Distance:  9  40  200"""
TESTS = [(1, SAMPLE, 288), (2, SAMPLE, 71503)]
# vim:expandtab:sw=4:ts=4
