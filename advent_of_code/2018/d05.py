#!/bin/python
"""Advent of Code, Day 5: Alchemical Reduction. Compute the length of a polymer after reactions."""
from lib import aoc


class Day05(aoc.Challenge):
    """Day 5: Alchemical Reduction."""

    TESTS = [
        aoc.TestCase(inputs="dabAcCaCBAcCcaDA", part=1, want=10),
        aoc.TestCase(inputs="dabAcCaCBAcCcaDA", part=2, want=4),
    ]

    DELTA = abs(ord("A") - ord("a"))

    def reduce(self, codepoints: list[int], ignore: set[int]) -> list[int]:
        """Return the remaining elements after pairs react away."""
        unreacted: list[int] = []
        for codepoint in codepoints:
            if codepoint in ignore:
                pass
            elif unreacted and abs(codepoint - unreacted[-1]) == self.DELTA:
                unreacted.pop()
            else:
                unreacted.append(codepoint)
        return unreacted

    def part1(self, puzzle_input: str) -> int:
        """Return the polymer length after reactions."""
        codepoints = [ord(i) for i in puzzle_input]
        return len(self.reduce(codepoints, set()))

    def part2(self, puzzle_input: str) -> int:
        """Return the polymer length after reactions with one element removed."""
        codepoints = [ord(i) for i in puzzle_input]
        # Pre-reduce once to avoid repeated work.
        codepoints = self.reduce(codepoints, set())
        ord_a, ord_z = ord("A"), ord("Z")
        candidates = {i for i in codepoints if ord_a <= i <= ord_z}
        return min(
            len(self.reduce(codepoints, {candidate, candidate + self.DELTA}))
            for candidate in candidates
        )
