#!/bin/python
"""Advent of Code, Day 16: Chronal Classification."""

from lib import aoc

SAMPLE = """\
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]

Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]



1 2 3 4"""

InputType = list[list[list[list[int]]] | list[list[int]]]


class Day16(aoc.Challenge):
    """Day 16: Chronal Classification. Map op instructions and simulate a CPU."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=2),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    # Split the input into the captures and program.
    # Split captures into single captures which are a set of 3*4 digits.
    INPUT_PARSER = aoc.ParseBlocks([aoc.ParseBlocks([aoc.parse_ints]), aoc.parse_ints], "\n" * 4)

    def compute(self, instruction: int, op_a: int, op_b: int, memory: list[int]) -> int:
        """Return the result of a single instruction."""
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
        """Return the number of instructions which map to three or more potential operations."""
        captures, _ = parsed_input
        return sum(
            sum(
                post[target] == self.compute(op, op_a, op_b, prior)
                for op in range(16)
            ) >= 3
            for prior, (_, op_a, op_b, target), post in captures
        )

    def part2(self, parsed_input: InputType) -> int:
        """Decode instruction mappings and run a program."""
        captures, program = parsed_input

        # Assume all mappings are possible. Then resolve via elimination.
        op_possibilities = {i: set(range(16)) for i in range(16)}
        op_map = {}  # Resolved operations.
        for prior, (instruction, op_a, op_b, target), post in captures:
            if instruction in op_map:
                # Optimization: do not check instructions we already resolved. 30ms => 20ms.
                continue
            candidates = {
                op
                for op in range(16)
                if post[target] == self.compute(op, op_a, op_b, prior)
            }
            op_possibilities[instruction] &= candidates
            if len(op_possibilities[instruction]) == 1:
                found = list(op_possibilities[instruction])[0]
                op_map[instruction] = found
                for other, candidates in op_possibilities.items():
                    if other != instruction and found in candidates:
                        candidates.remove(found)

        # Run the program.
        memory = [0] * 4
        for instruction, op_a, op_b, target in program:
            memory[target] = self.compute(op_map[instruction], op_a, op_b, memory)
        return memory[0]

# vim:expandtab:sw=4:ts=4
