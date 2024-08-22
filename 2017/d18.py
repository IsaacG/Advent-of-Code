#!/bin/python
"""Advent of Code, Day 18: Duet."""
from __future__ import annotations

import collections
import dataclasses
import functools
import itertools
import math
import re

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

LineType = int
InputType = list[LineType]


@dataclasses.dataclass
class Program:

    program: list[list]
    program_id: int
    q_send: collections.deque
    q_recv: collections.deque

    def __post_init__(self) -> None:
        self.registers = collections.defaultdict(int)
        self.registers["p"] = self.program_id
        self.ptr = 0
        self.sent = 0

    def val(self, register: int | str) -> int:
        if isinstance(register, int):
            return register
        return self.registers[register]

    def run(self) -> bool:
        sent = False
        while True:
            match self.program[self.ptr]:
                case ["snd", X]:
                    self.q_send.append(self.val(X))
                    sent = True
                    self.sent += 1
                case ["set", X, Y]:
                    self.registers[X] = self.val(Y)
                case ["add", X, Y]:
                    self.registers[X] += self.val(Y)
                case ["mul", X, Y]:
                    self.registers[X] *= self.val(Y)
                case ["mod", X, Y]:
                    self.registers[X] %= self.val(Y)
                case ["rcv", X]:
                    if not self.q_recv:
                        return sent
                    self.registers[X] = self.q_recv.popleft()
                case ["jgz", X, Y]:
                    if self.val(X) > 0:
                        self.ptr += self.val(Y) - 1
            self.ptr += 1


class Day18(aoc.Challenge):
    """Day 18: Duet."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=4),
        aoc.TestCase(part=2, inputs=SAMPLE[1], want=3),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    # INPUT_PARSER = aoc.parse_multi_str_per_line
    INPUT_PARSER = aoc.parse_multi_mixed_per_line

    def part1(self, parsed_input: InputType) -> int:
        print("\n".join(["==="] + [f"{k}={v!r}" for k, v in locals().items()] + ["==="]))
        registers = collections.defaultdict(int)

        def val(register: int | str) -> int:
            if isinstance(register, int):
                return register
            return registers[register]

        mem = parsed_input
        ptr = 0
        last_played = 0
        for step in range(5000):
            # print(step, ptr, mem[ptr][0], mem[ptr][1:], [val(i) for i in mem[ptr][1:]])
            match mem[ptr]:
                case ["snd", X]:
                    last_played = val(X)
                case ["set", X, Y]:
                    registers[X] = val(Y)
                case ["add", X, Y]:
                    registers[X] += val(Y)
                case ["mul", X, Y]:
                    registers[X] *= val(Y)
                case ["mod", X, Y]:
                    registers[X] %= val(Y)
                case ["rcv", X]:
                    if val(X):
                        return last_played
                case ["jgz", X, Y]:
                    if val(X) > 0:
                        ptr += val(Y) - 1
            ptr += 1

    def part2(self, parsed_input: InputType) -> int:
        q_a, q_b = collections.deque(), collections.deque()
        programs = [
            Program(parsed_input, 0, q_a, q_b),
            Program(parsed_input, 1, q_b, q_a),
        ]
        while any([p.run() for p in programs]):
            pass
        return programs[1].sent

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().input_parser(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]
        # Words: mixed str and int
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in line.split()
            )
            for line in puzzle_input.splitlines()
        ]
        # Regex splitting
        patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in patt.match(line).groups()
            )
            for line in puzzle_input.splitlines()
        ]

# vim:expandtab:sw=4:ts=4
