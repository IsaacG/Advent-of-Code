#!/bin/python
"""Advent of Code, Day 23: Safe Cracking. Simulate a computer."""

from lib import aoc

SAMPLE = """\
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a"""

InputType = list[list[str]]


class Day23(aoc.Challenge):
    """Day 23: Safe Cracking."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=3),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]
    PARAMETERIZED_INPUTS = [7, 12]

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        """Simulate a computer."""
        instructions = [line.split() for line in parsed_input]
        end = len(instructions)
        register = {i: 0 for i in "abcd"}
        register["a"] = param
        ptr = 0

        def multiply():
            """Handle a multiplication loop efficiently.

            4: ["cpy", "b", "c"]
            5: ["inc", "a"]  a += b * d
            6: ["dec", "c"]
            7: ["jnz", "c", "-2"]
            8: ["dec", "d"]
            9: ["jnz", "d", "-5"]
            """
            nonlocal ptr
            var_b, var_c = instructions[ptr][1:]
            var_a = instructions[ptr + 1][1]
            var_d = instructions[ptr + 4][1]
            want = [
                ["cpy", var_b, var_c],
                ["inc", var_a],
                ["dec", var_c],
                ["jnz", var_c, "-2"],
                ["dec", var_d],
                ["jnz", var_d, "-5"],
            ]
            if instructions[ptr:ptr + 6] != want:
                return False
            register[var_a] += register[var_c] * register[var_d]
            register[var_c] = register[var_d] = 0
            ptr += 5
            return True

        def decrement_or_addition():
            """Handle an addition loop efficiently.

            5: ["dec", "b"]
            6: ["inc", "a"]
            7: ["jnz", "b", "-2"]

            Note, lines 5, 6 could be swapped and are not handled.
            """
            nonlocal ptr
            var_b, var_a = instructions[ptr][1], instructions[ptr + 1][1]
            want = [
                ["dec", var_b],
                ["inc", var_a],
                ["jnz", var_b, "-2"],
            ]
            if instructions[ptr:ptr + 3] != want:
                register[var_b] -= 1
                return
            register[var_a] += register[var_b]
            register[var_b] = 0
            ptr += 2

        while ptr < end:
            match instructions[ptr]:
                case ["cpy", val, dst]:
                    value = int(val) if aoc.RE_INT.match(val) else register[val]
                    register[dst] = value
                    multiply()
                case ["inc", dst]:
                    register[dst] += 1
                case ["dec", dst]:
                    decrement_or_addition()
                case ["jnz", val, distance]:
                    cond = int(val) if aoc.RE_INT.match(val) else register[val]
                    jump = int(distance) if aoc.RE_INT.match(distance) else register[distance]
                    if cond != 0:
                        ptr += jump - 1
                case ["tgl", val]:
                    loc = ptr + register[val]
                    if 0 <= loc < end:
                        old = instructions[loc]
                        if len(old) == 2:
                            old[0] = "dec" if old[0] == "inc" else "inc"
                        if len(old) == 3:
                            old[0] = "cpy" if old[0] == "jnz" else "jnz"
            ptr += 1

        return register["a"]
