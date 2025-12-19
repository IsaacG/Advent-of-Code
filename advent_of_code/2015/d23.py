#!/bin/python
"""Advent of Code, Day 23: Opening the Turing Lock. Emulate a simple CPU."""
from __future__ import annotations

from lib import aoc

SAMPLE = """\
inc b
jio b, +2
tpl b
inc b"""


def line_parser(line: str):
    """Parse one line of input."""
    return [int(i) if aoc.RE_INT.match(i) else i for i in line.replace(",", "").split()]


PARSER = aoc.ParseOneWordPerLine(line_parser)


def solve(data: list[list[int | str]], part: int) -> int:
    """Emulate a program and return register "b"."""
    ptr = 0
    max_inst = len(data) - 1
    registers = {"a": 0 if part == 1 else 1, "b": 0}

    while 0 <= ptr <= max_inst:
        jump_offset = 1
        match data[ptr]:
            case ["hlf", reg]:
                registers[str(reg)] //= 2
            case ["tpl", reg]:
                registers[str(reg)] *= 3
            case ["inc", reg]:
                registers[str(reg)] += 1
            case ["jmp", offset]:
                jump_offset = int(offset)
            case ["jie", reg, offset]:
                if registers[str(reg)] % 2 == 0:
                    jump_offset = int(offset)
            case ["jio", reg, offset]:
                if registers[str(reg)] == 1:
                    jump_offset = int(offset)
        ptr += jump_offset
    return registers["b"]


TESTS = [(1, SAMPLE, 2)]
