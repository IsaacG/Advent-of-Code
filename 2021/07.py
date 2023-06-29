#!/bin/python
"""Advent of Code: Day 07."""

from typing import Callable
import typer

from lib import aoc

InputType = list[list[int]]

SAMPLE = "16,1,2,0,4,2,7,1,2,14"


class Day07(aoc.Challenge):
    """Solve the optimal positioning for crab-submarine blasting."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=37),
        aoc.TestCase(inputs=SAMPLE, part=2, want=168),
    )
    INPUT_PARSER = aoc.parse_re_findall_int(aoc.RE_INT)
    PARAMETERIZED_INPUTS = [
        # Return the optimal blast position with constant movement cost.
        lambda x: x,
        # Return the optimal blast position with linear movement cost.
        lambda x: x * (x + 1) // 2,
    ]

    def solver(self, parsed_input: list[int], func: Callable[[int], int]) -> int:
        """Find the location where it is cheapest for all the crabs to move."""
        positions = parsed_input[0]
        costs = []
        for i in range(min(positions), max(positions) + 1):
            costs.append(sum(func(abs(i - pos)) for pos in positions))
        return min(costs)


if __name__ == "__main__":
    typer.run(Day07().run)
