#!/bin/python
"""Advent of Code: Day 01. Examine the sea floor depth to determine how many values are increases."""


def solve(data: list[int], part: int) -> int:
    """Return the number of "steps" with an increase."""
    if part == 2:
        # Use a rolling window (summed) for steps.
        # Same as part1 but use a rolling sum of three elements for each step.
        data = [a + b + c for a, b, c in zip(data, data[1:], data[2:])]

    # Given a list of numbers, count how many of those elements are increases
    # (greater than) the prior element.
    return sum(b > a for a, b in zip(data, data[1:]))


SAMPLE = "199 200 208 210 200 207 240 269 260 263".replace(" ", "\n")
TESTS = ((1, SAMPLE, 7), (2, SAMPLE, 5))
