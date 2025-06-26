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

    def solver(self, puzzle_input: str, part_one: bool) -> int:
        """Return the sum of all the multiplications."""
        puzzle_input = puzzle_input.replace("\n", " ")
        if not part_one:
            # Remove any don't()-do() pairs and any trailing don't().
            puzzle_input = re.sub(r"don't\(\).*?(do\(\)|$)", "", puzzle_input)
        return sum(
            int(a) * int(b)
            for a, b in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", puzzle_input)
        )

# vim:expandtab:sw=4:ts=4
