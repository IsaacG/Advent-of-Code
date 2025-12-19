#!/bin/python
"""Advent of Code, Day 12: Leonardo's Monorail. Simulate a computer."""

from lib import aoc
import assembunny

OP_CPY = assembunny.Operation.CPY.value
OP_INC = assembunny.Operation.INC.value
OP_DEC = assembunny.Operation.DEC.value
OP_JNZ = assembunny.Operation.JNZ.value

SAMPLE = """\
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""


class Day12(aoc.Challenge):
    """Day 12: Leonardo's Monorail."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=42),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]
    TIMEOUT = 45

    def solver(self, puzzle_input: list[str], part_one: bool) -> int:
        """Simulate a computer."""
        instructions = []
        for instruction in puzzle_input:
            op_code = assembunny.Operation[instruction[0].upper()].value
            instructions.append([op_code] + instruction[1:])
        end = len(instructions)
        register = {i: 0 for i in "abcd"}
        if not part_one:
            register["c"] = 1

        def value(arg: str | int) -> int:
            return arg if isinstance(arg, int) else register[arg]

        ptr = 0
        while ptr < end:
            operation, *args = instructions[ptr]
            if operation == OP_CPY:
                register[args[1]] = value(args[0])
            elif operation == OP_INC:
                register[args[0]] += 1
            elif operation == OP_DEC:
                register[args[0]] -= 1
            elif operation == OP_JNZ and value(args[0]):
                ptr += value(args[1]) - 1
            ptr += 1

        return register["a"]
