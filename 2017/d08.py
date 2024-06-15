#!/bin/python
"""Advent of Code, Day 8: I Heard You Like Registers."""
from __future__ import annotations

import collections
import functools
import itertools
import operator
import re

from lib import aoc

SAMPLE = """\
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""

LineType = int
InputType = list[LineType]


class Day08(aoc.Challenge):
    """Day 8: I Heard You Like Registers."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=1),
        aoc.TestCase(inputs=SAMPLE, part=2, want=10),
    ]
    INPUT_PARSER = aoc.parse_multi_str_per_line

    def part1(self, parsed_input: list[list[str]]) -> int:
        registers = collections.defaultdict(int)
        for target_reg, action, action_amount, _, test_reg, test_op, test_amount in parsed_input:
            if aoc.OPERATORS[test_op](registers[test_reg], int(test_amount)):
                target_op = {"dec": operator.sub, "inc": operator.add}[action]
                registers[target_reg] = target_op(registers[target_reg], int(action_amount))
        return max(registers.values())

    def part2(self, parsed_input: list[list[str]]) -> int:
        largest = 0
        registers = collections.defaultdict(int)
        for target_reg, action, action_amount, _, test_reg, test_op, test_amount in parsed_input:
            if aoc.OPERATORS[test_op](registers[test_reg], int(test_amount)):
                target_op = {"dec": operator.sub, "inc": operator.add}[action]
                result = target_op(registers[target_reg], int(action_amount))
                largest = max(largest, result)
                registers[target_reg] = result
        return largest

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().input_parser(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]
        # Words: mixed str and int
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in line.split()
            )
            for line in puzzle_input.splitlines()
        ]
        # Regex splitting
        patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in patt.match(line).groups()
            )
            for line in puzzle_input.splitlines()
        ]

# vim:expandtab:sw=4:ts=4
