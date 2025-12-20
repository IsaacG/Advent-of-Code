#!/bin/python
"""Advent of Code, Day 17: Spinlock."""


def solve(data: int, part: int) -> int:
    """Return the value after 2017/50M step-inserts."""
    step = data
    pos = 0

    if part == 1:
        vals = [0]
        for i in range(1, 2017 + 1):
            pos = (pos + step) % i + 1
            vals.insert(pos % (i + 1), i)
        return vals[(pos + 1) % len(vals)]

    last_insert = 0
    for i in range(1, 50000000 + 1):
        pos = ((pos + step) % i) + 1
        if pos == 1:
            last_insert = i

    return last_insert


TESTS = [(1, "3", 638)]
# vim:expandtab:sw=4:ts=4
