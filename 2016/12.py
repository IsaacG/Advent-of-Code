#!/bin/python
"""Advent of Code, Day 12: Leonardo's Monorail. Simulate a computer."""

from lib import aoc

SAMPLE = """\
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""


class Day12(aoc.Challenge):
    """Day 12: Leonardo's Monorail."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=42),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]
    TIMEOUT = 45

    def solver(self, parsed_input: list[str], param: bool) -> int:
        """Simulate a computer."""
        instructions = [line.split() for line in parsed_input]
        end = len(instructions)
        register = {i: 0 for i in "abcd"}
        if param:
            register["c"] = 1

        ptr = 0
        while ptr < end:
            match instructions[ptr]:
                case ["cpy", val, dst]:
                    if val.isnumeric():
                        register[dst] = int(val)
                    else:
                        register[dst] = register[val]
                case ["inc", dst]:
                        register[dst] += 1
                case ["dec", dst]:
                        register[dst] -= 1
                case ["jnz", val, distance]:
                    cond = int(val) if val.isnumeric() else register[val]
                    if cond != 0:
                        ptr += int(distance) - 1
            ptr += 1

        return register["a"]
