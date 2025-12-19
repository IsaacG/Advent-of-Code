#!/bin/python
"""Advent of Code, Day 1: Not Quite Lisp. Count Santa's floor level."""
MAPPING = {"(": 1, ")": -1}


def solve(data: str, part: int) -> int:
    """Return Santa's final floor and when he gets to the basement."""
    if part == 1:
        return sum(MAPPING[i] for i in data)

    floor = 0
    for count, i in enumerate(data, start=1):
        floor += MAPPING[i]
        if floor == -1:
            return count
    raise RuntimeError("No solution found.")


TESTS = [
    (1, "(())", 0),
    (1, "()()", 0),
    (1, "(()(()(", 3),
    (2, ")", 1),
    (2, "()())", 5),
]
