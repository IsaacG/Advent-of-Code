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
        """Compute a path through a firewall scanner.

        Each scanner has a fixed number of locations it can be at.
        The location is cyclic and we only care if it is in the top position or not.
        If we "unwrap" the path, it can be viewed as a cyclic path, eg (0 1 2 1 0) -> (0 1 2 3 0).
        The position can be computed as (picoseconds % interval) where the second half of the cycle
        maps to to the first half but in an upwards direction.

        Given that we only care if `(picoseconds % interval) == 0` and not the actual position,
        we don't need to track the position.
        We just need the interval `(range - 1) * 2.
        """
        ranges: dict[int, int] = dict(sorted(parsed_input))  # type: ignore
        intervals = {depth: (range_ - 1) * 2 for depth, range_ in ranges.items()}

        # Part one: sum(range * depth) for each sensor that would catch us (i.e. position == 0).
        if part_one:
            return sum(
                ranges[depth] * depth
                for depth, interval in intervals.items()
                if depth % interval == 0
            )

        # Part two: return the smallest delay for which we can avoid being caught.
        # Note, convert intervals to a list for faster iteration.
        intervals_list = list(intervals.items())
        return next(
            delay
            for delay in itertools.count()
            if all((delay + depth) % interval for depth, interval in intervals_list)
        )

# vim:expandtab:sw=4:ts=4
