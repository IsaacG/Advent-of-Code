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
        traps = {i for i, char in enumerate(parsed_input) if char == "^"}

        rows = 10 if self.testing else 40
        if param:
            rows = 400_000

        safe = 0
        for _ in range(rows):
            safe += width - len(traps)
            traps = {
                col
                for col in range(width)
                if (col - 1 in traps) != (col + 1 in traps)
            }

        return safe
