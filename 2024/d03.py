#!/bin/python
"""Advent of Code, Day 3: Mull It Over."""

import re
from lib import aoc

SAMPLE = [
    'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))',
    "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))",
]

class Day03(aoc.Challenge):
    """Day 3: Mull It Over."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=161),
        aoc.TestCase(part=2, inputs=SAMPLE[1], want=48),
    ]
    INPUT_PARSER = aoc.parse_one_str

    def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:
        """Return the sum of all the multiplications."""
        if not part_one:
            # Account for do() and don't() instructions.
            parts = puzzle_input.split("don't()")
            t = [p for p in parts[1:] if "do()" in p]
            t = [p.split("do()", 1)[1] for p in t]
            puzzle_input = parts[0] + "".join(t)
        return sum(
            int(a) * int(b)
            for a, b in re.findall(r"mul\((\d+),(\d+)\)", puzzle_input)
        )

# vim:expandtab:sw=4:ts=4
