#!/bin/python
"""Advent of Code, Day 5: Alchemical Reduction. Compute the length of a polymer after reactions."""
from lib import aoc

DELTA = abs(ord("A") - ord("a"))


def reduce(codepoints: list[int], ignore: set[int]) -> list[int]:
    """Return the remaining elements after pairs react away."""
    unreacted: list[int] = []
    for codepoint in codepoints:
        if codepoint in ignore:
            pass
        elif unreacted and abs(codepoint - unreacted[-1]) == DELTA:
            unreacted.pop()
        else:
            unreacted.append(codepoint)
    return unreacted


def solve(data: str, part: int) -> int:
    """Return the polymer length after reactions."""
    if part == 1:
        codepoints = [ord(i) for i in data]
        return len(reduce(codepoints, set()))

    codepoints = [ord(i) for i in data]
    # Pre-reduce once to avoid repeated work.
    codepoints = reduce(codepoints, set())
    ord_a, ord_z = ord("A"), ord("Z")
    candidates = {i for i in codepoints if ord_a <= i <= ord_z}
    return min(
        len(reduce(codepoints, {candidate, candidate + DELTA}))
        for candidate in candidates
    )


TESTS = [(1, "dabAcCaCBAcCcaDA", 10), (2, "dabAcCaCBAcCcaDA", 4)]
