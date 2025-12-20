#!/bin/python
"""Advent of Code, Day 8: I Heard You Like Registers."""

import collections
import operator

from lib import aoc


def solve(data: list[list[str]], part: int) -> int:
    """Apply conditional logic to update registers."""
    largest = 0
    registers: dict[str, int] = collections.defaultdict(int)
    for target_reg, action, action_amount, _, test_reg, test_op, test_amount in data:
        if aoc.OPERATORS[test_op](registers[test_reg], int(test_amount)):
            target_op = {"dec": operator.sub, "inc": operator.add}[action]
            result = target_op(registers[target_reg], int(action_amount))
            largest = max(largest, result)
            registers[target_reg] = result

    if part == 1:
        return max(registers.values())
    return largest


SAMPLE = """\
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""
TESTS = [(1, SAMPLE, 1), (2, SAMPLE, 10)]
# vim:expandtab:sw=4:ts=4
