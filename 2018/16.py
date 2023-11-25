#!/bin/python
"""Advent of Code, Day 16: Chronal Classification."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = """\
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]

Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]



1 2 3 4"""

LineType = int
InputType = list[LineType]


class Day16(aoc.Challenge):
    """Day 16: Chronal Classification."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=2),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.ParseBlocks([aoc.ParseBlocks([aoc.parse_ints]), aoc.parse_ints], "\n" * 4)

    def compute(self, instruction: int, op_a: int, op_b: int, memory: list[int]) -> int:
        match instruction:
            case 0:
                # addr (add register) stores into register C the result of adding register A and register B.
                return memory[op_a] + memory[op_b]
            case 1:
                # addi (add immediate) stores into register C the result of adding register A and value B.
                return memory[op_a] + op_b
            case 2:
                # mulr (multiply register) stores into register C the result of multiplying register A and register B.
                return memory[op_a] * memory[op_b]
            case 3:
                # muli (multiply immediate) stores into register C the result of multiplying register A and value B.
                return memory[op_a] * op_b
            case 4:
                # banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
                return memory[op_a] & memory[op_b]
            case 5:
                # bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
                return memory[op_a] & op_b
            case 6:
                # borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
                return memory[op_a] | memory[op_b]
            case 7:
                # bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
                return memory[op_a] | op_b
            case 8:
                # setr (set register) copies the contents of register A into register C. (Input B is ignored.)
                return memory[op_a]
            case 9:
                # seti (set immediate) stores value A into register C. (Input B is ignored.)
                return op_a
            case 10:
                # gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
                return 1 if op_a > memory[op_b] else 0
            case 11:
                # gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
                return 1 if memory[op_a] > op_b else 0
            case 12:
                # gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
                return 1 if memory[op_a] > memory[op_b] else 0
            case 13:
                # eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
                return 1 if op_a == memory[op_b] else 0
            case 14:
                # eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
                return 1 if memory[op_a] == op_b else 0
            case 15:
                # eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
                return 1 if memory[op_a] == memory[op_b] else 0
            case _:
                raise ValueError("Unknown instruction")

    def part1(self, parsed_input: InputType) -> int:
        captures, program = parsed_input

        for prior, (instruction, op_a, op_b, target), post in captures:
            a = prior.copy()
            b = post.copy()
            del a[target]
            del b[target]
            assert a == b

        count = sum(
            sum(
                post[target] == self.compute(op, op_a, op_b, prior)
                for op in range(16)
            ) >= 3
            for prior, (_, op_a, op_b, target), post in captures
        )
        assert count != 85
        return count

    def part2(self, parsed_input: InputType) -> int:
        captures, program = parsed_input
        op_mapping = {i: set(range(16)) for i in range(16)}
        for prior, (instruction, op_a, op_b, target), post in captures:
            candidates = {
                op
                for op in range(16)
                if post[target] == self.compute(op, op_a, op_b, prior)
            }
            if len(candidates) == 0:
                raise RuntimeError("Failed to find a candidate")
            op_mapping[instruction] &= candidates
            if len(op_mapping[instruction]) == 1:
                found = list(op_mapping[instruction])[0]
                for other, candidates in op_mapping.items():
                    if other != instruction and found in candidates:
                        candidates.remove(found)
        if sum(len(candidates) == 1 for candidates in op_mapping.values()) != 16:
            raise RuntimeError("Could not decode instructions.")

        op_map = {i: list(candidates)[0] for i, candidates in op_mapping.items()}
        memory = [0] * 4
        for instruction, op_a, op_b, target in program:
            memory[target] = self.compute(op_map[instruction], op_a, op_b, memory)
        return memory[0]

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
