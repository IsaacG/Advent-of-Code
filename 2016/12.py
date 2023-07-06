#!/bin/python
"""Advent of Code, Day 12: Leonardo's Monorail. Simulate a computer."""

import enum
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

    def solver(self, parsed_input: list[str], param: bool) -> int:
        """Simulate a computer."""
        instructions = []
        for line in parsed_input:
            instruction = line.split()
            instructions.append([assembunny.Operation[instruction[0].upper()].value] + instruction[1:])
        end = len(instructions)
        register = {i: 0 for i in "abcd"}
        if param:
            register["c"] = 1

        def value(arg):
            return int(arg) if aoc.RE_INT.match(arg) else register[arg]

        ptr = 0
        while ptr < end:
            op, *args = instructions[ptr]
            if op == OP_CPY:
                register[args[1]] = value(args[0])
            elif op == OP_INC:
                register[args[0]] += 1
            elif op == OP_DEC:
                register[args[0]] -= 1
            elif op == OP_JNZ and value(args[0]):
                ptr += value(args[1]) - 1
            ptr += 1

        return register["a"]
