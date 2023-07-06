#!/bin/python
"""Advent of Code, Day 25: Clock Signal."""

import collections
import functools
import itertools
import math
import re

from lib import aoc


INSTRUCTIONS = {
    "inc": 1,
    "dec": 2,
    "jnz": 3,
    "tgl": 4,
    "out": 5,
    "cpy": 6,
}


class Day25(aoc.Challenge):
    """Day 25: Clock Signal."""

    DEBUG = True
    TESTS = [
        aoc.TestCase(inputs="", part=1, want=aoc.TEST_SKIP),
        aoc.TestCase(inputs="", part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        """Simulate a computer."""
        instructions = [line.split() for line in parsed_input]
        return next(
            i for i in itertools.count()
            if self.simulate(instructions, i)
        )

    def simulate(self, instructions, val_a) -> bool:
        end = len(instructions)
        register = {i: 0 for i in "bcd"}
        register["a"] = val_a
        ptr = 0
        prior_states = set()

        def state():
            """Tuple representing the current state of the computer, used for cycle checking.

            The instruction args and immutable, so they do not need to be checked.
            What changes in the state is (1) the register values and (2) the instructions (word 1).
            """
            instruction_state = 0
            for instruction in instructions:
                instruction_state = instruction_state * 8 + INSTRUCTIONS[instruction[0]]
            return (instruction_state,) + tuple(register.values())

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

        last_out = None

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
                case ["out", var]:
                    val = register[var]
                    if last_out is None:
                        last_out = val
                    elif 1 - val != last_out:
                        # If we generate the wrong signal, abort.
                        return False
                    else:
                        # Toggle the output signal.
                        last_out = val
                        # Check for a cycle.
                        new_state = state()
                        if new_state in prior_states:
                            return True
                        prior_states.add(new_state)
                case ["tgl", val]:
                    loc = ptr + register[val]
                    if 0 <= loc < end:
                        old = instructions[loc]
                        if len(old) == 2:
                            old[0] = "dec" if old[0] == "inc" else "inc"
                        if len(old) == 3:
                            old[0] = "cpy" if old[0] == "jnz" else "jnz"
                case _:
                    raise RuntimeError(f"Could not parse {instructions[ptr]}")
            ptr += 1

        # Failed to find a cycle.
        return False
