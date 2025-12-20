#!/bin/python
"""Advent of Code, Day 12: Leonardo's Monorail. Simulate a computer."""

import assembunny

OP_CPY = assembunny.Operation.CPY.value
OP_INC = assembunny.Operation.INC.value
OP_DEC = assembunny.Operation.DEC.value
OP_JNZ = assembunny.Operation.JNZ.value


def solve(data: list[list[str]], part: int) -> int:
    """Simulate a computer."""
    instructions = []
    for instruction in data:
        op_code = assembunny.Operation[instruction[0].upper()].value
        instructions.append([op_code] + instruction[1:])
    end = len(instructions)
    register = {i: 0 for i in "abcd"}
    if part == 2:
        register["c"] = 1

    def value(arg: str | int) -> int:
        return arg if isinstance(arg, int) else register[arg]

    ptr = 0
    while ptr < end:
        operation, *args = instructions[ptr]
        if operation == OP_CPY:
            register[str(args[1])] = value(args[0])
        elif operation == OP_INC:
            register[str(args[0])] += 1
        elif operation == OP_DEC:
            register[str(args[0])] -= 1
        elif operation == OP_JNZ and value(args[0]):
            ptr += value(args[1]) - 1
        ptr += 1

    return register["a"]


SAMPLE = """\
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""
TESTS = [(1, SAMPLE, 42)]
