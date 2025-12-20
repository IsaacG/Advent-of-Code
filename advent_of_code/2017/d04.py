#!/bin/python
"""Advent of Code, Day 4: High-Entropy Passphrases. Count valid passphrases."""
import itertools


def solve(data: list[list[str]], part: int) -> int:
    """Count valid passphrases."""
    # Check where no word is repeated.
    if part == 1:
        return sum(len(set(line)) == len(line) for line in data)

    # Check no word is an anagram of another.
    return sum(
        all(sorted(a) != sorted(b) for a, b in itertools.combinations(line, 2))
        for line in data
    )


SAMPLE = [
    """\
aa bb cc dd ee
aa bb cc dd aa
aa bb cc dd aaa""",
    """\
abcde fghij
abcde xyz ecdab
a ab abc abd abf abj
iiii oiii ooii oooi oooo
oiii ioii iioi iiio"""
]
TESTS = [(1, SAMPLE[0], 2), (2, SAMPLE[1], 3)]
# vim:expandtab:sw=4:ts=4
