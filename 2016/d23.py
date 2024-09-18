#!/bin/python
"""Advent of Code, Day 23: Safe Cracking. Simulate a computer."""

import assembunny
from lib import aoc

SAMPLE = """\
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a"""


class Day23(aoc.Challenge):
    """Day 23: Safe Cracking."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=3),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]

    def solver(self, puzzle_input: list[str], part_one: bool) -> int:
        """Simulate a computer."""
        computer = assembunny.Assembunny(puzzle_input)
        return computer.run(register_a=7 if part_one else 12)[0]
