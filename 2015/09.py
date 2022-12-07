#!/bin/python
"""Advent of Code: Day 09."""

import collections
import functools
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = ["""\
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""]

LineType = tuple[str, str, int]
InputType = list[LineType]
LINE_RE = re.compile(r"^(.+) to (.+) = (\d+)$")


class Day09(aoc.Challenge):
    """Day 9: All in a Single Night."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=605),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=982),
    ]

    def distances(self, parsed_input: InputType) -> list[int]:
        distances = {}
        locations: set[str] = set()
        for src, dst, dist in parsed_input:
            distances[src, dst] = dist
            distances[dst, src] = dist
            locations.add(src)
            locations.add(dst)

        def cost(order: tuple[str, ...]) -> int:
            return sum(
                distances[src, dst]
                for src, dst in zip(order, order[1:])
            )

        return [
            cost(order)
            for order in itertools.permutations(locations, len(locations))
        ]

    def part1(self, parsed_input: InputType) -> int:
        return min(self.distances(parsed_input))

    def part2(self, parsed_input: InputType) -> int:
        return max(self.distances(parsed_input))

    def line_parser(self, line: str) -> LineType:
        """If defined, use this to parse single lines."""
        src, dst, dist = LINE_RE.match(line).groups()
        return (src, dst, int(dist))


if __name__ == "__main__":
    typer.run(Day09().run)

# vim:expandtab:sw=4:ts=4
