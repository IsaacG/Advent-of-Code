#!/bin/python
"""Advent of Code, Day 18: Like a Rogue. Return the number of safe tiles."""

from lib import aoc


class Day18(aoc.Challenge):
    """Day 18: Like a Rogue."""

    TESTS = [
        aoc.TestCase(inputs=".^^.^.^^^^", part=1, want=38),
        aoc.TestCase(inputs="", part=2, want=aoc.TEST_SKIP),
    ]

    def solver(self, parsed_input: str, param: bool) -> int:
        """Return the number of safe tiles."""
        width = len(parsed_input)
        width_mask = (1 << (width)) - 1

        rows = 10 if self.testing else 40
        if param:
            rows = 400_000

        traps = 0
        for i, char in enumerate(reversed(parsed_input)):
            if char == "^":
                traps |= 1 << i

        safe = 0
        for row in range(rows):
            safe += width - traps.bit_count()
            traps = ((traps << 1) ^ (traps >> 1)) & width_mask

        return safe
