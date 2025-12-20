#!/bin/python
"""Advent of Code, Day 25: Let It Snow. Compute the code needed to start the machine."""

from lib import aoc


def solve(data: list[list[int]], part: int) -> int:
    """Return the code given on a row/column."""
    del part
    row, column = data[0]
    # Determine the code generation number based on row/column.
    code_num = 1
    for i in range(1, row):
        code_num += i
    for i in range(row + 1, row + column):
        code_num += i
    # Starting code, given in the puzzle.
    code = 20151125
    # Generate new codes n times until we get the one we need.
    for i in range(code_num - 1):
        code = (code * 252533) % 33554393
    return code


PARSER = aoc.parse_ints
TESTS = [
    (1, "1 1", 20151125),
    (1, "2 6", 4041754),
    (1, "6 4", 24659492),
]
