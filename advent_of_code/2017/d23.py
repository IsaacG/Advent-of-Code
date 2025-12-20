#!/bin/python
"""Advent of Code, Day 23: Coprocessor Conflagration."""

import math
from lib import aoc
PARSER = aoc.parse_multi_mixed_per_line


def solve(data: list[list[str | int]], part: int) -> int:
    """Simulate a program and count multiplications."""
    if part == 2:
        # Return the number of non-primes in a range. Derived by analysis."""
        return sum(
            1
            for b in range(105700, 122700 + 1, 17)
            if any(b % i == 0 for i in range(2, math.ceil(math.sqrt(b))))
        )

    code = data
    ptr = 0
    mul_count = 0
    registers = {i: 0 for i in "abcdefgh"}

    def val(register: int | str) -> int:
        """Return a value, either an immediate value or register lookup."""
        if isinstance(register, int):
            return register
        return registers[register]

    while True:
        try:
            instructions = code[ptr]
        except IndexError:
            return mul_count
        ptr += 1
        match instructions:
            case ["set", str() as arg_x, arg_y]:
                registers[arg_x] = val(arg_y)
            case ["sub", str() as arg_x, arg_y]:
                registers[arg_x] -= val(arg_y)
            case ["mul", str() as arg_x, arg_y]:
                mul_count += 1
                registers[arg_x] *= val(arg_y)
            case ["jnz", arg_x, arg_y] if val(arg_x) != 0:
                ptr += val(arg_y) - 1
    raise RuntimeError("No solution found.")


TESTS = list[tuple[int, int, int]]()
# vim:expandtab:sw=4:ts=4
