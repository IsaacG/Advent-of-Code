#!/bin/python
"""Advent of Code, Day 17: No Such Thing as Too Much. Count ways to fill containers."""

import collections
import itertools

import typer
from lib import aoc

SAMPLE = """\
20
15
10
5
5"""

LineType = int
InputType = list[LineType]


class Day17(aoc.Challenge):
    """Day 17: No Such Thing as Too Much."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=4),
        aoc.TestCase(inputs=SAMPLE, part=2, want=3),
    ]
    INPUT_PARSER = aoc.parse_one_int_per_line

    def solver(self, containers: list[int]) -> dict[int, int]:
        """Compute the number of ways to fill containers."""
        target = 25 if self.testing else 150
        count: dict[int, int] = collections.defaultdict(int)
        for number in range(len(containers)):
            for combo in itertools.combinations(containers, number):
                if sum(combo) == target:
                    count[number] += 1
        return count

    def part1(self, parsed_input: InputType) -> int:
        """Return the possible countainer combos which fit the eggnog."""
        return sum(self.solver(parsed_input).values())

    def part2(self, parsed_input: InputType) -> int:
        """Return the possible countainer combos which use the min number of containers."""
        count = self.solver(parsed_input)
        return count[min(count)]


if __name__ == "__main__":
    typer.run(Day17().run)

# vim:expandtab:sw=4:ts=4
