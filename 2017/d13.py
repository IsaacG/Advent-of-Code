#!/bin/python
"""Advent of Code, Day 13: Packet Scanners."""

import itertools
from lib import aoc

SAMPLE = """\
0: 3
1: 2
4: 4
6: 4"""


class Day13(aoc.Challenge):
    """Day 13: Packet Scanners."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=24),
        aoc.TestCase(part=2, inputs=SAMPLE, want=10),
    ]
    PARAMETERIZED_INPUTS = [True, False]
    INPUT_PARSER = aoc.parse_ints_per_line

    def solver(self, parsed_input: list[list[int]], part_one: bool) -> int:
        """Compute a path through a firewall scanner."""
        depths, ranges = [], []
        for depth, range_ in sorted(parsed_input):
            depths.append(depth)
            ranges.append(range_)
        positions = [
            itertools.cycle(list(range(n)) + list(range(n - 2, 0, -1)))
            for n in ranges
        ]

        for depth, position in zip(depths, positions):
            for _ in range(depth):
                next(position)

        if part_one:
            return sum(
                range_ * depth
                for range_, depth, position in zip(ranges, depths, positions)
                if next(position) == 0
            )

        for offset in itertools.count():
            if all([next(position) for position in positions]):
                return offset

# vim:expandtab:sw=4:ts=4
