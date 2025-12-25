#!/bin/python
"""Day 1: Chronal Calibration.

Sum up frequencies then do so repeatedly until a repeat is seen.
"""
import itertools


def solve(data: list[int], part: int) -> int:
    if part == 1:
        return sum(data)
    seen = set()
    freq = 0
    it = itertools.cycle(data)
    while freq not in seen:
        seen.add(freq)
        freq += next(it)
    return freq


TESTS = [
    (1, "+1 -2 +3 +1".replace(" ", "\n"), 3),
    (1, "+1 +1 +1".replace(" ", "\n"), 3),
    (1, "+1 +1 -2".replace(" ", "\n"), 0),
    (1, "-1 -2 -3".replace(" ", "\n"), -6),
    (2, "+1 -2 +3 +1".replace(" ", "\n"), 2),
    (2, "+1 -1".replace(" ", "\n"), 0),
    (2, "+3 +3 +4 -2 -4".replace(" ", "\n"), 10),
    (2, "-6 +3 +8 +5 -6".replace(" ", "\n"), 5),
    (2, "+7 +7 -2 -7 -4".replace(" ", "\n"), 14),
]
