#!/bin/python
"""Advent of Code: Day 07."""

from typing import Callable

from lib import aoc

InputType = list[list[int]]

SAMPLE = "16,1,2,0,4,2,7,1,2,14"


class Day07(aoc.Challenge):
    """Solve the optimal positioning for crab-submarine blasting."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=37),
        aoc.TestCase(inputs=SAMPLE, part=2, want=168),
    )

    def solver(self, puzzle_input: list[int], part_one: bool) -> int:
        """Find the location where it is cheapest for all the crabs to move."""
        positions = puzzle_input[0]
        costs = []
        # Return the optimal blast position with constant movement cost.
        # Return the optimal blast position with linear movement cost.
        func = (lambda x: x) if part_one else (lambda x: x * (x + 1) // 2)
        for i in range(min(positions), max(positions) + 1):
            costs.append(sum(func(abs(i - pos)) for pos in positions))
        return min(costs)
