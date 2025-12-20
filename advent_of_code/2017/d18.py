#!/bin/python
"""Advent of Code, Day 18: Duet.  Simulate parallel programs with bidirectional communication."""

import collections
import collections.abc
import itertools

from lib import aoc


def program(
    code: list[list[str | int]],
    program_id: int,
    part: int,
) -> collections.abc.Generator[list[int], list[int], int]:
    """Run a program with IO queues.

    Part 1 returns the last snd value on rcv non-zero.
    Part 2 yields on a rcv and returns the total send count.
    """
    registers = collections.defaultdict(int)
    registers["p"] = program_id
    ptr = 0
    sent = 0
    outputs: list[int] = []
    inputs = yield outputs
    q_in = collections.deque(inputs)

    def val(register: int | str) -> int:
        """Return a value, either an immediate value or register lookup."""
        if isinstance(register, int):
            return register
        return registers[register]

    while True:
        instructions = code[ptr]
        ptr += 1
        match instructions:
            case ["set", str() as arg_x, arg_y]:
                registers[arg_x] = val(arg_y)
            case ["add", str() as arg_x, arg_y]:
                registers[arg_x] += val(arg_y)
            case ["mul", str() as arg_x, arg_y]:
                registers[arg_x] *= val(arg_y)
            case ["mod", str() as arg_x, arg_y]:
                registers[arg_x] %= val(arg_y)
            case ["jgz", arg_x, arg_y] if val(arg_x) > 0:
                ptr += val(arg_y) - 1
            case ["snd", arg_x]:
                outputs.append(val(arg_x))
                sent += 1
            case ["rcv", arg_x] if part == 1 and val(arg_x):
                # Part one. On the first non-zero rcv, return the last send value.
                return outputs.pop()
            case ["rcv", str() as arg_x] if part == 2:
                # Yield if we are out of values.
                # If we have recv values, read one.
                # If we yielded and still do not have values, return the sent count.
                if not q_in:
                    inputs = yield outputs
                    outputs = []
                    q_in.extend(inputs)
                    if not inputs:
                        return sent
                registers[arg_x] = q_in.popleft()


def solve(data: list[list[str | int]], part: int) -> int:
    """Run two programs and get IO details."""
    # Create two programs.
    programs = {i: program(data, i, part) for i in range(2)}
    # Initialize then run the programs.
    next(programs[0])
    vals = next(programs[1])
    for i in itertools.cycle(programs):
        try:
            vals = programs[i].send(vals)
        except StopIteration as e:
            # On a StopIteration, handle the return value.
            if part == 1 or i == 1:
                return e.value
    raise RuntimeError


INPUT_PARSER = aoc.parse_multi_mixed_per_line
SAMPLE = [
    """\
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2""",
    """\
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d""",
]
TESTS = [(1, SAMPLE[0], 4), (2, SAMPLE[1], 3)]
# vim:expandtab:sw=4:ts=4
