#!/bin/python
"""Advent of Code, Day 21: Chronal Conversion."""

import typing
from lib import aoc


def compute(bound: int, instructions: list[tuple[str, int, int, int]]) -> int:
    """Run a CPU simulator and report stop steps."""
    registers = [0] * 6

    mem_size = len(instructions)
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
            case ["bani", a, b, c]:
                registers[c] = registers[a] & b
            case ["bori", a, b, c]:
                registers[c] = registers[a] | b
            case _:
                raise RuntimeError(f"Unhandled instruction, {instruction}")
        ip = registers[bound] + 1

    return registers[0]


class Day21(aoc.Challenge):
    """Day 21: Chronal Conversion."""

    TESTS = [
        aoc.TestCase(part=1, inputs="", want=aoc.TEST_SKIP),
        aoc.TestCase(part=2, inputs="", want=aoc.TEST_SKIP),
    ]

    def part1(self, puzzle_input: list[list[str | int]]) -> int:
        """Return the r0 value needed to make the program terminate."""
        reg, *instructions = puzzle_input
        # Instruction 28 compares r0 and r3 and halts if they match
        # Insert an instruction that copies r3 to r0.
        # Then the compare matches and r0 is returned -- the answer we want.
        instructions.insert(28, ["setr", 3, 0, 0])
        return compute(bound=int(reg[1]), instructions=typing.cast(list[tuple[str, int, int, int]], instructions))

    def part2(self, puzzle_input: list[list[str | int]]) -> int:
        """Reverse engineer the program. Run until no new values are discovered."""
        seen = set()
        last_new_value = 0
        r2, r3 = 0, 0
        prior_states = set()
        while (r2, r3) not in prior_states:
            prior_states.add((r2, r3))
            r2 = r3 | 65536
            r3 = 832312
            while r2 > 0:
                r2, mod = divmod(r2, 256)
                r3 = (((r3 + mod) & 16777215) * 65899) & 16777215
            if r3 not in seen:
                seen.add(r3)
                last_new_value = r3
        return last_new_value

# vim:expandtab:sw=4:ts=4
