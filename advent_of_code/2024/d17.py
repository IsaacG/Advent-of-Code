#!/bin/python
"""Advent of Code, Day 17: Chronospatial Computer."""

import itertools
from lib import aoc

InputType = tuple[list[int], list[int]]
PARSER = aoc.ParseBlocks([aoc.ParseIntergers()])

def simulate(reg: dict[str, int], instructions: list[int]) -> list[int]:
    """Simulate a CPU."""
    ptr = 0

    def val(i):
        if 0 <= i <= 3:
            return i
        return reg[{4: "A", 5: "B", 6: "C"}[i]]

    out = []
    while ptr + 1 < len(instructions):
        instruction, op = instructions[ptr:ptr + 2]
        ptr += 2
        match instruction:
            case 0: # adv
                reg["A"] = reg["A"] // (2 ** val(op))
            case 1: # bxl
                reg["B"] = reg["B"] ^ op
            case 2: # bst
                reg["B"] = val(op) % 8
            case 3 if reg["A"] != 0: # jnz
                ptr = op
            case 4: # bxc
                reg["B"] = reg["B"] ^ reg["C"]
            case 5: # out
                out.append((val(op) % 8))
            case 6: # bdv
                reg["B"] = reg["A"] // (2 ** val(op))
            case 7: # cdv
                reg["C"] = reg["A"] // (2 ** val(op))

    return out


def solve(data: InputType, part: int, testing: bool) -> int:
    """Compute the initial A value to make a program a quine."""
    reg_vals, instructions = data
    registers = {char: reg_vals[i] for i, char in enumerate("ABC")}
    if part == 1:
        return ",".join(str(i) for i in simulate(registers, instructions))

    # Naive brute force. Doesn't work on the real input.
    if testing:
        # Speed up the tests by jumping towards the solution.
        for i in itertools.count(start=100_000):
            registers["A"] = i
            got = simulate(registers.copy(), instructions)
            if got == instructions:
                return i

    def simulate2(reg_a: int) -> list[int]:
        """Simulate the program but faster. Reverse engineered from my program."""
        out = []
        while reg_a:
            shift = reg_a & 7 ^ 7
            digit = (3 ^ reg_a ^ (reg_a >> shift)) & 7
            out.append(digit)
            reg_a = reg_a >> 3
        return out

    def solve(given: int, output_pos: int, preserve: int) -> int | None:
        """Solve for the next digit of the output.

        Each output digit is composed on the right-most (3 bit) byte, int_one,
        and a second byte, int_two.
        The int_two is found (int_one ^ 7) bits from the right.
        For instance, 0b101_010_101 has int_one = 101 = 5.
        int_two is located 101 ^ 7 = 101 ^ 111 = 010 = 2 bits to the left.
        Shifting by two gives 10_1 = 101 = 5 as int_two.
        The output is 3 ^ int_one ^ int_two.
        This function brute forces by trying all possible values for int_one.
        Given int_one, we can brute force int_two by setting int_two = digit ^ 3 ^ int_one.
        After shifting int_two over and adding it to the number, we need to ensure int_one wasn't overwritten.

        As an optimization, the preserve bits are used to track which bits are "set" and should
        not be updated/overwritten to compute over digits.
        """
        given <<= 3
        preserve <<= 3
        candidates = set()
        want_output = instructions[output_pos]  # The output want_output we want to generate.
        for int_one in range(8):
            shift = int_one ^ 7
            int_two = want_output ^ 3 ^ int_one

            # Combine the two ints.
            # If we shift by less than 3, check they do not overwrite each other.
            # They might "line up" and share space eg 101 << 1 and 100.
            combined_ints = (int_two << shift) | int_one
            if shift < 3 and (
                combined_ints & 7 != int_one or (combined_ints >> shift) & 7 != int_two
            ):
                continue

            new_num = given | combined_ints
            # Check we didn't overwrite preserved bits from a prior digit.
            if given & preserve != new_num & preserve:
                continue

            # Run the simulator to ensure we get the correct digits.
            got = simulate2(new_num)
            if len(got) == len(instructions) - output_pos and got == instructions[output_pos:]:
                # Record the new number as a candidate, along with the updated preserve mask.
                candidates.add((new_num, preserve | 7 | (7 << shift)))

        reg_a_vals: set[int]
        if output_pos == 0:
            # We got all digits. Select the min candidate.
            reg_a_vals = {i[0] for i in candidates}
        else:
            # Try using the number to generate the next digit(s).
            reg_a_vals = set()
            for option, new_preserve in candidates:
                if (next_step := solve(option, output_pos - 1, new_preserve)) is not None:
                    reg_a_vals.add(next_step)
        return min(reg_a_vals) if reg_a_vals else None

    result = solve(0, len(instructions) - 1, 0)
    if result is None:
        raise RuntimeError("No solution found.")
    return result


SAMPLE = [
    """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0""",  # 76
    """\
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""
]
TESTS = [(1, SAMPLE[0], "4,6,3,5,6,3,5,2,1,0"), (2, SAMPLE[1], 117440)]
# vim:expandtab:sw=4:ts=4
