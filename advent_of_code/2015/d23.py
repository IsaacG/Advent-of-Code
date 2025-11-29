#!/bin/python
"""Advent of Code, Day 23: Opening the Turing Lock. Emulate a simple CPU."""
from __future__ import annotations

from lib import aoc

SAMPLE = """\
inc b
jio b, +2
tpl b
inc b"""

LineType = list[int | str]
InputType = list[LineType]


class Day23(aoc.Challenge):
    """Day 23: Opening the Turing Lock."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=2),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]

    @staticmethod
    def line_parser(line: str):
        """Parse one line of input."""
        return [int(i) if aoc.RE_INT.match(i) else i for i in line.replace(",", "").split()]

    INPUT_PARSER = aoc.ParseOneWordPerLine(line_parser)

    def solver(self, instructions: InputType, part_one: bool) -> int:
        """Emulate a program and return register "b"."""
        ptr = 0
        max_inst = len(instructions) - 1
        registers = {"a": 0 if part_one else 1, "b": 0}

        while 0 <= ptr <= max_inst:
            jump_offset = 1
            match instructions[ptr]:
                case ["hlf", reg]:
                    registers[reg] //= 2
                case ["tpl", reg]:
                    registers[reg] *= 3
                case ["inc", reg]:
                    registers[reg] += 1
                case ["jmp", offset]:
                    jump_offset = offset
                case ["jie", reg, offset]:
                    if registers[reg] % 2 == 0:
                        jump_offset = offset
                case ["jio", reg, offset]:
                    if registers[reg] == 1:
                        jump_offset = offset
                case _:
                    raise ValueError(f"Invalid instruction, {instructions[ptr]}")
            ptr += jump_offset
        return registers["b"]
