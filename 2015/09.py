#!/bin/python
"""Advent of Code: Day 09. All in a Single Night."""

import itertools
import re

from lib import aoc

SAMPLE = ["""\
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""]

InputType = list[int]
LINE_RE = re.compile(r"^(.+) to (.+) = (\d+)$")


class Day09(aoc.Challenge):
    """Day 9: Compute the cost of visiting all cities.."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=605),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=982),
    ]

    def part1(self, parsed_input: InputType) -> int:
        """Return the shortest route."""
        return min(parsed_input)

    def part2(self, parsed_input: InputType) -> int:
        """Return the longest route."""
        return max(parsed_input)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input and generate the total cost for each route."""
        distances = {}
        locations: set[str] = set()
        for line in puzzle_input.splitlines():
            src, dst, dist_raw = LINE_RE.match(line).groups()
            dist = int(dist_raw)

            distances[src, dst] = dist
            distances[dst, src] = dist
            locations.add(src)
            locations.add(dst)

        return [
            sum(
                distances[src, dst]
                for src, dst in zip(order, order[1:])
            )
            for order in itertools.permutations(locations, len(locations))
        ]
