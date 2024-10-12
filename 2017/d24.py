#!/bin/python
"""Advent of Code, Day 24: Electromagnetic Moat."""

import functools
from lib import aoc

SAMPLE = """\
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""


class Day24(aoc.Challenge):
    """Day 24: Electromagnetic Moat."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=31),
        aoc.TestCase(part=2, inputs=SAMPLE, want=19),
    ]
    INPUT_PARSER = aoc.parse_ints_per_line

    def strongest(self, start: int, options: set[tuple[int, int]]) -> tuple[int, int, int]:
        strength = 0
        longest_length = 0
        longest_strength = 0

        for option in options:
            if start not in option:
                continue
            cur = option[0] + option[1]
            next_start = cur - start
            n_str, n_len, n_long_str = self.strongest(next_start, options - {option})
            strength = max(strength, n_str + cur)
            n_long_str += cur
            if n_len > longest_length:
                longest_length = n_len
                longest_strength = n_long_str
            elif n_len == longest_length and n_long_str > longest_strength:
                longest_strength = n_long_str
        return strength, longest_length + 1, longest_strength

    def solver(self, puzzle_input: list[list[int]], part_one: bool) -> int:
        """Compute the strongest (longest) magnetic bridge which can be built."""
        data = {tuple(i) for i in puzzle_input}
        return self.strongest(0, data)[0 if part_one else 2]

# vim:expandtab:sw=4:ts=4
