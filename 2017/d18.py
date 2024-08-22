#!/bin/python
"""Advent of Code, Day 18: Duet."""

import collections
import collections.abc
import itertools

from lib import aoc

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


def program(
    code: list[list[str | int]],
    program_id: int,
    q_send: collections.deque,
    q_recv: collections.deque,
    part_one: bool
) -> collections.abc.Generator[None, None, int]:
    """Run a program with IO queues.

    Part 1 returns the last snd value on rcv non-zero.
    Part 2 yields on a rcv and returns the total send count.
    """
    registers = collections.defaultdict(int)
    registers["p"] = program_id
    ptr = 0
    sent = 0

    def val(register: int | str) -> int:
        """Return a value, either an immediate value or register lookup."""
        if isinstance(register, int):
            return register
        return registers[register]

    while True:
        instructions = code[ptr]
        ptr += 1
        match instructions:
            case ["set", str(X), Y]:
                registers[X] = val(Y)
            case ["add", str(X), Y]:
                registers[X] += val(Y)
            case ["mul", str(X), Y]:
                registers[X] *= val(Y)
            case ["mod", str(X), Y]:
                registers[X] %= val(Y)
            case ["jgz", X, Y] if val(X) > 0:
                ptr += val(Y) - 1
            case ["snd", X]:
                q_send.append(val(X))
                sent += 1
            case ["rcv", X] if part_one and val(X):
                # Part one. On the first non-zero rcv, return the last send value.
                return q_send.pop()
            case ["rcv", str(X)] if not part_one:
                # Yield if we are out of values.
                # If we have recv values, read one.
                # If we yielded and still do not have values, return the sent count.
                if not q_recv:
                    yield
                    if not q_recv:
                        return sent
                registers[X] = q_recv.popleft()


class Day18(aoc.Challenge):
    """Day 18: Duet. Simulate parallel programs with bidirectional communication."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=4),
        aoc.TestCase(part=2, inputs=SAMPLE[1], want=3),
    ]
    INPUT_PARSER = aoc.parse_multi_mixed_per_line
    PARAMETERIZED_INPUTS = [True, False]

    def solver(self, parsed_input: list[list[str | int]], param: bool) -> int:
        """Run two programs and get IO details."""
        # Create queues for communication in both directions.
        q_a: collections.deque[int] = collections.deque()
        q_b: collections.deque[int] = collections.deque()
        # Create two programs.
        programs = [
            program(parsed_input, 0, q_a, q_b, param),
            program(parsed_input, 1, q_b, q_a, param),
        ]
        # Run the programs.
        for i in itertools.count():
            try:
                next(programs[i % 2])
            except StopIteration as e:
                # On a StopIteration, handle the return value.
                if param or i % 2 == 1:
                    return e.value
        raise RuntimeError

# vim:expandtab:sw=4:ts=4
