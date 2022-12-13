#!/bin/python
"""Advent of Code, Day 23: Opening the Turing Lock."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = [
    """\
inc b
jio b, +2
tpl b
inc b"""
]

LineType = int
InputType = list[LineType]


class Day23(aoc.Challenge):
    """Day 23: Opening the Turing Lock."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=2),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def solver(self, instructions: InputType, start_a: int) -> int:
        ptr = 0
        max_inst = len(instructions) - 1
        reg = {"a": start_a, "b": 0}

        step = 1
        while 0 <= ptr <= max_inst and step < 10000:
            step += 1
            match instructions[ptr]:
                case ["hlf", r]:
                    ptr += 1
                    reg[r] //= 2
                case ["tpl", r]:
                    ptr += 1
                    reg[r] *= 3
                case ["inc", r]:
                    ptr += 1
                    reg[r] += 1
                case ["jmp", offset]:
                    ptr += offset
                case ["jie", r, offset]:
                    ptr += offset if reg[r] % 2 == 0 else 1
                case ["jio", r, offset]:
                    ptr += offset if reg[r] == 1 else 1
                case _:
                    raise ValueError(f"Invalid instruction, {instructions[ptr]}")
        return reg["b"]

    def part1(self, parsed_input: InputType) -> int:
        return self.solver(parsed_input, 0)

    def part2(self, parsed_input: InputType) -> int:
        return self.solver(parsed_input, 1)

    def line_parser(self, line: str):
        return [int(i) if aoc.RE_INT.match(i) else i for i in line.replace(",", "").split()]


if __name__ == "__main__":
    typer.run(Day23().run)

# vim:expandtab:sw=4:ts=4
