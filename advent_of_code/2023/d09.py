#!/bin/python
"""Advent of Code, Day 9: Mirage Maintenance."""


def get_prior_and_following(line) -> tuple[int, int]:
    """Return the prior and following value of a line using recursive first differences."""
    diffs = [b - a for a, b in zip(line, line[1:])]
    if all(i == 0 for i in diffs):
        prior = following = 0
    else:
        prior, following = get_prior_and_following(diffs)
    return line[0] - prior, line[-1] + following


def solve(data: list[list[int]], part: int) -> int:
    """Compute the next value in a series using repeated first differences."""
    # Sum up the prior or following value from each line.
    return sum(
        get_prior_and_following(line)[1 if part == 1 else 0]
        for line in data
    )


SAMPLE = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
TESTS = [(1, SAMPLE, 114), (2, SAMPLE, 2)]
# vim:expandtab:sw=4:ts=4
