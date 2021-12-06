#!/bin/python
"""Advent of Code: Day 06."""

import collections

import typer

from lib import aoc

SAMPLE = "3,4,3,1,2"

InputType = list[int]


class Day06(aoc.Challenge):
    """Compute how many lantern fish there are, after they breed."""

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=5934),
        aoc.TestCase(inputs=SAMPLE, part=2, want=26984457539),
    )

    def part1(self, lines: InputType) -> int:
        """Compute fish population after 80 days."""
        return self.solve(lines, 80)

    def part2(self, lines: InputType) -> int:
        """Compute fish population after 256 days."""
        return self.solve(lines, 256)

    @staticmethod
    def solve(lines: InputType, days: int) -> int:
        """Compute fish population after N days."""
        # Construct the initial population map. Age -> count.
        counter = dict(collections.Counter(lines))
        for _ in range(days):
            # Reduce day counter for all fish.
            new = {k - 1: v for k, v in counter.items() if k}
            # Add new baby fish and reset the counter on fish that spawned.
            new[6] = counter.get(0, 0) + counter.get(7, 0)
            new[8] = counter.get(0, 0)
            counter = new
        return sum(counter.values())

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data. Comma separated ints."""
        return [int(i) for i in puzzle_input.split(",")]


if __name__ == "__main__":
    typer.run(Day06().run)
