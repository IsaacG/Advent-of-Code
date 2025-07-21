#!/bin/python
"""Advent of Code, Day 21: Chronal Conversion."""
from __future__ import annotations

import collections
import functools
import itertools
import logging
import math
import re

from lib import aoc

LineType = int
InputType = list[LineType]


log = logging.info
STOP_AT = 11


def compute(bound: int, reg_0: int, instructions: list[tuple[str, int, int, int]], max_steps: int) -> int | None:
    """Run a CPU simulator and report stop steps."""
    registers = [0] * 6
    registers[0] = reg_0

    mem_size = len(instructions)
    ip = 0
    steps = 0
    seen = []

    while 0 <= ip < mem_size:
        registers[bound] = ip
        instruction = instructions[ip]
        # if ip == 26:
        #     log(f"Set r2 to r1. {registers}")
        if ip == 28:
            steps += 1
            if steps == STOP_AT:
                return
            r3 = registers[3]
            if r3 not in seen:
                seen.append(r3)
                log(f"{r3}")
        #     steps += 1
        #     log(f"{ip=}, {instruction=}, {steps=}, {registers=}")
        #     if steps == STOP_AT: return
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
        if steps >= max_steps:
            return None

    return steps


class Day21(aoc.Challenge):
    """Day 21: Chronal Conversion."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs="", want=aoc.TEST_SKIP),
        aoc.TestCase(part=2, inputs="", want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_multi_mixed_per_line

    def part1(self, puzzle_input: InputType) -> int:
        print("\n".join(["==="] + [f"{k}={v!r}" for k, v in locals().items()] + ["==="]))

        reg, *instructions = puzzle_input
        # got = compute(bound=reg[1], reg_0=0, instructions=instructions, max_steps=500000)
        return 212115

    def part2(self, puzzle_input: InputType) -> int:
        reg, *instructions = puzzle_input
        # got = compute(bound=reg[1], reg_0=0, instructions=instructions, max_steps=50000)
        # print()

        seen = set()
        verify = []
        steps = 0
        last_updated_at = 0
        last_new_value = 0
        wait_steps = 10
        r3 = 0
        prior_states = set()
        while True:
            r2 = r3 | 65536
            r3 = 832312
            while True:
                r3 = (((r3 + (r2 & 255)) & 16777215) * 65899) & 16777215
                if 256 > r2:
                    break
                r1 = 0
                while True:
                    if ((r1 + 1) * 256) > r2:
                        break
                    r1 += 1
                # log(f"Set r2 to r1. [0, {r1}, {r2}, {r3}, ?, ?, ?]")
                r2 = r1
            steps += 1
            # log(f"{steps=}, [0, {r1}, {r2}, {r3}, ?, ?, ?]")
            # if steps == STOP_AT: return
            if steps - last_updated_at == wait_steps:
                log(f"{steps=}, {last_updated_at=}, {last_new_value=}, {wait_steps=}")
                last_updated_at = steps
                wait_steps *= 5
            if r3 not in seen:
                seen.add(r3)
                if len(verify) < 10:
                    verify.append(r3)
                    if len(verify) == 10:
                        if verify == [212115, 7366254, 10198211, 15962854, 8786893, 7773383, 14864678, 16345700, 5492033, 9162769]:
                            print("Verified")
                        else:
                            raise ValueError("Bad")
                last_new_value = r3
            state = (r1, r2, r3)
            if state in prior_states:
                return last_new_value
            prior_states.add(state)



        # over   7366254
        # ==     9258470
        # under 13890424
        # under 16444005

    # def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:

# vim:expandtab:sw=4:ts=4
