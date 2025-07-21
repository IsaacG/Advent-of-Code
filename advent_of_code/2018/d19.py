#!/bin/python
"""Advent of Code, Day 19: Go With The Flow."""
from __future__ import annotations

import collections
import functools
import itertools
import logging
import math
import re

from lib import aoc

SAMPLE = [
    """\
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5""",
]

LineType = int
InputType = list[LineType]


def log(*args, **kwargs) -> None:
    logging.info(*args, **kwargs)

class Day19(aoc.Challenge):
    """Day 19: Go With The Flow."""

    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=6),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_multi_mixed_per_line

    def compute(self, puzzle_input: InputType, initial: int) -> int:
        registers = [0] * 6
        registers[0] = initial
        setup, *instructions = puzzle_input
        mem_size = len(instructions)
        assert setup[0] == "#ip"
        bound = setup[1]
        ip = 0
        steps = 0

        while 0 <= ip < mem_size:
            steps += 1
            if steps % 500000 == 0:
                log(f"{steps=} {ip=} {registers=}")
            registers[bound] = ip
            # pre = f"{ip=} {registers}"
            instruction = instructions[ip]
            if ip == 1:
                log("LOOP START:", registers)
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
            # post = " ".join(str(i) for i in instruction)
            # log(f"{pre} {post} {registers}")
            ip = registers[bound] + 1
        
        return registers[0]

    def part1(self, puzzle_input: InputType) -> int:
        if self.testing:
            return self.compute(puzzle_input, 0)
        c = 882
        return sum(b for b in range(1, c + 1) if c % b == 0)

    def part2(self, puzzle_input: InputType) -> int:
        if self.testing:
            return self.compute(puzzle_input, 1)
        c = 10551282
        return sum(b for b in range(1, c + 1) if c % b == 0)


    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        got = super().input_parser(puzzle_input)
        setup, *instructions = got
        mem_size = len(instructions)
        assert setup[0] == "#ip"
        bound = setup[1]
        regs = "abcdef"
        for idx, (op, a, b, c) in enumerate(instructions):
            out = regs[c]
            if a < 6:
                ra = regs[a]
            if b < 6:
                rb = regs[b]
                selfop = out in {ra, rb}
                if ra == rb == out:
                    other = out
                elif selfop:
                    other = ({ra, rb} - {out,}).pop()

            match op:
                case "seti":
                    if c == bound:
                        log(f"{idx:2}  {op:5} {a:2}  _ {c:2}  #  GOTO {a + 1}")
                    else:
                        log(f"{idx:2}  {op:5} {a:2}  _ {c:2}  #  {out} = {a}")
                case "setr":
                    if c == bound:
                        log(f"{idx:2}  {op:5} {a:2}  _ {c:2}  #  GOTO {ra} + 1")
                    else:
                        log(f"{idx:2}  {op:5} {a:2}  _ {c:2}  #  {out} = {ra}")
                case "addi":
                    if c == bound:
                        assert a == c
                        log(f"{idx:2}  {op:5} {a:2} {b:2} {c:2}  #  GOTO +{b + 1}")
                    elif a == c:
                        log(f"{idx:2}  {op:5} {a:2} {b:2} {c:2}  #  {out} += {b}")
                    else:
                        log(f"{idx:2}  {op:5} {a:2} {b:2} {c:2}  #  {out} = {ra} + {b}")
                case "addr":
                    if c == bound:
                        assert selfop
                        log(f"{idx:2}  {op:5} {a:2} {b:2} {c:2}  #  JUMP {other}")
                    elif selfop:
                        log(f"{idx:2}  {op:5} {a:2} {b:2} {c:2}  #  {out} += {other}")
                    else:
                        log(f"{idx:2}  {op:5} {a:2} {b:2} {c:2}  #  {out} = {ra} + {rb}")
                case "muli":
                    if c == bound:
                        assert a == c
                        log(f"{idx:2}  {op:5} {a:2} {b:2} {c:2}  #  GOTO *{b}")
                    elif a == c:
                        log(f"{idx:2}  {op:5} {a:2} {b:2} {c:2}  #  {out} *= {b}")
                    else:
                        log(f"{idx:2}  {op:5} {a:2} {b:2} {c:2}  #  {out} = {ra} * {b}")
                case "mulr":
                    if c == bound:
                        assert a == b == c and idx * idx > len(instructions)
                        log(f"{idx:2}  {op:5} {a:2} {b:2} {c:2}  #  HALT")
                    elif a == c:
                        log(f"{idx:2}  {op:5} {a:2} {b:2} {c:2}  #  {out} *= {rb}")
                    else:
                        log(f"{idx:2}  {op:5} {a:2} {b:2} {c:2}  #  {out} = {ra} * {rb}")
                case "eqrr":
                    assert c != bound
                    log(f"{idx:2}  {op:5} {a:2} {b:2} {c:2}  #  {out} = ({ra} == {rb})")
                case "gtrr":
                    assert c != bound
                    log(f"{idx:2}  {op:5} {a:2} {b:2} {c:2}  #  {out} = ({ra} > {rb})")
                case _:
                    raise RuntimeError(f"Unhandled instruction, {instruction}")
        return got

# vim:expandtab:sw=4:ts=4
