#!/bin/python
"""Advent of Code, Day 6: Trash Compactor."""
from lib import aoc
PARSER = str


def solve(data: str, part: int) -> int:
    """Return the answer for the math homework."""
    if part == 1:
        words = [line.split() for line in data.splitlines()]
        return sum(
            aoc.LIST_OPS[op](int(i) for i in nums)
            for *nums, op in zip(*words)
        )
    *nums, ops = data.splitlines()
    longest_line = max(len(i) for i in data.splitlines())
    starts = [idx for idx, char in enumerate(ops) if char != " "] + [longest_line + 1]
    operators = ops.split()

    total = 0
    for start, end, op in zip(starts, starts[1:], operators):
        # Collect all columns.
        numbers = [
            int(
                # Collect all lines for one column.
                "".join(
                    line[col] for line in nums if line[col] != " "
                )
            )
            for col in range(start, end - 1)
        ]
        total += aoc.LIST_OPS[op](numbers)
    return total


SAMPLE = """\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
TESTS = [(1, SAMPLE, 4277556), (2, SAMPLE, 3263827)]
# vim:expandtab:sw=4:ts=4
