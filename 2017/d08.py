#!/bin/python
"""Advent of Code, Day 8: I Heard You Like Registers."""

import collections
import operator

from lib import aoc

SAMPLE = """\
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""


class Day08(aoc.Challenge):
    """Day 8: I Heard You Like Registers."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=1),
        aoc.TestCase(inputs=SAMPLE, part=2, want=10),
    ]
    INPUT_PARSER = aoc.parse_multi_str_per_line

    def solver(self, puzzle_input: list[list[str]], part_one: bool) -> int:
        """Apply conditional logic to update registers."""
        largest = 0
        registers: dict[str, int] = collections.defaultdict(int)
        for target_reg, action, action_amount, _, test_reg, test_op, test_amount in puzzle_input:
            if aoc.OPERATORS[test_op](registers[test_reg], int(test_amount)):
                target_op = {"dec": operator.sub, "inc": operator.add}[action]
                result = target_op(registers[target_reg], int(action_amount))
                largest = max(largest, result)
                registers[target_reg] = result

        if part_one:
            return max(registers.values())
        return largest

# vim:expandtab:sw=4:ts=4
