#!/bin/python
"""Advent of Code, Day 19: Go With The Flow."""

import typing


def compute(data: list[list[str | int]], initial: int) -> int:
    """Run a CPU simulator."""
    registers = [0] * 6
    registers[0] = initial
    setup = typing.cast(tuple[str, int], data[0])
    instructions = typing.cast(list[tuple[str, int, int, int]], data[1:])
    mem_size = len(instructions)
    assert setup[0] == "#ip"

    bound = setup[1]
    ip = 0

    while 0 <= ip < mem_size:
        registers[bound] = ip
        instruction = instructions[ip]
        match instruction:
            case ["seti", a, _, c]:
                registers[c] = a
            case ["setr", a, _, c]:
                registers[c] = registers[a]
            case ["addi", a, b, c]:
                registers[c] = registers[a] + b
            case ["addr", a, b, c]:
                registers[c] = registers[a] + registers[b]
            case ["muli", a, b, c]:
                registers[c] = registers[a] * b
            case ["mulr", a, b, c]:
                registers[c] = registers[a] * registers[b]
            case ["eqir", a, b, c]:
                registers[c] = 1 if a == registers[b] else 0
            case ["eqri", a, b, c]:
                registers[c] = 1 if registers[a] == b else 0
            case ["eqrr", a, b, c]:
                registers[c] = 1 if registers[a] == registers[b] else 0
            case ["gtrr", a, b, c]:
                registers[c] = 1 if registers[a] > registers[b] else 0
            case ["gtir", a, b, c]:
                registers[c] = 1 if a > registers[b] else 0
            case ["gtri", a, b, c]:
                registers[c] = 1 if registers[a] > b else 0
            case _:
                raise RuntimeError(f"Unhandled instruction, {instruction}")
        ip = registers[bound] + 1

    return registers[0]


def solve(data: list[list[str | int]], part: int, testing: bool) -> int:
    if testing:
        return compute(data, 0 if part == 1 else 1)
    # Reverse engineer the program. Sum of factors.
    # Run the program to extract the upper limit:
    limit = 882 if part == 1 else 10551282
    return sum(factor for factor in range(1, limit + 1) if limit % factor == 0)


SAMPLE = """\
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""
TESTS = [(1, SAMPLE, 6)]
# vim:expandtab:sw=4:ts=4
