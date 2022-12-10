#!/bin/python
"""Advent of Code: Day 07."""

from typing import Callable
import typer

from lib import aoc

InputType = list[int]

SAMPLE = "16,1,2,0,4,2,7,1,2,14"


class Day07(aoc.Challenge):
    """Solve the optimal positioning for crab-submarine blasting."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=37),
        aoc.TestCase(inputs=SAMPLE, part=2, want=168),
    )

    def part1(self, parsed_input: InputType) -> int:
        """Return the optimal blast position with constant movement cost."""
        return self.solver(parsed_input, lambda x: x)

    def part2(self, parsed_input: InputType) -> int:
        """Return the optimal blast position with linear movement cost."""
        return self.solver(parsed_input, lambda x: x * (x + 1) // 2)

    @staticmethod
    def solver(positions: list[int], func: Callable[[int], int]) -> int:
        """Find the location where it is cheapest for all the crabs to move."""
        costs = []
        for i in range(min(positions), max(positions) + 1):
            costs.append(sum(func(abs(i - pos)) for pos in positions))
        return min(costs)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data. Comma separated ints."""
        return [int(i) for i in puzzle_input.split(",")]


if __name__ == "__main__":
    typer.run(Day07().run)
