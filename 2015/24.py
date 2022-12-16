#!/bin/python
"""Advent of Code, Day 24: It Hangs in the Balance. Balance numbers into groups with contraints."""

import itertools

import typer
from lib import aoc

SAMPLE = "\n".join([str(i) for i in list(range(1, 6)) + list(range(7, 12))])

LineType = int
InputType = list[LineType]


class Day24(aoc.Challenge):
    """Day 24: It Hangs in the Balance."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=99),
        aoc.TestCase(inputs=SAMPLE, part=2, want=44),
    ]
    INPUT_PARSER = aoc.parse_one_int_per_line

    def balance(self, packages: list[int], groups: int) -> int:
        """Return the group of packages which meets the constraints."""
        group_size = sum(packages) // groups
        candidates = []
        for package_count in range(1, len(packages)):
            for group in itertools.combinations(packages, package_count):
                if sum(group) == group_size:
                    candidates.append(self.mult(group))
            if candidates:
                break
        return min(candidates)

    def part1(self, parsed_input: InputType) -> int:
        """Return the smallest group, with 3 groups."""
        return self.balance(parsed_input, 3)

    def part2(self, parsed_input: InputType) -> int:
        """Return the smallest group, with 4 groups."""
        return self.balance(parsed_input, 4)


if __name__ == "__main__":
    typer.run(Day24().run)

# vim:expandtab:sw=4:ts=4
