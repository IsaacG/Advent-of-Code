#!/bin/python
"""Advent of Code, Day 18: Like a Rogue. Return the number of safe tiles."""


def solve(data: str, part: int, testing: bool) -> int:
    """Return the number of safe tiles."""
    width = len(data)
    width_mask = (1 << (width)) - 1

    rows = 10 if testing else 40 if part == 1 else 400_000

    traps = 0
    for i, char in enumerate(reversed(data)):
        if char == "^":
            traps |= 1 << i

    safe = 0
    for _ in range(rows):
        safe += width - traps.bit_count()
        traps = ((traps << 1) ^ (traps >> 1)) & width_mask

    return safe


TESTS = [(1, ".^^.^.^^^^", 38)]
