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
        ranges = dict(sorted(parsed_input))
        # This builds a dict of position generators.
        # If a sensor range is 4, it cycles through positions "0 1 2 3 2 1".
        # The two range() functions yield "0 1 2" and "3 2 1".
        # Using itertools.cycle() to generate positions is efficient.
        positions = {
            depth: itertools.cycle(list(range(range_ - 1)) + list(range(range_ - 1, 0, -1)))
            for depth, range_ in ranges.items()
        }

        # Rather than advancing all the sensors one step at a time,
        # we can store the sensor position at the moment we pass through that depth.
        # Advance all sensors by their depth to compute the position-at-passing-through.
        for depth, position in positions.items():
            for _ in range(depth):
                next(position)

        if part_one:
            # Part one: sum(range * depth) for each sensor that would catch us (ie position == 0).
            return sum(
                range_ * depth
                for depth, range_ in ranges.items()
                if next(positions[depth]) == 0
            )

        # Part two: return the smallest delay for which we can avoid being caught.
        # Note: Using a list is 10-20% faster than using the dict_values.
        # Note: We need to pass a list to all() to ensure next() is called on all elements.
        position_iterators = list(positions.values())
        for delay in itertools.count():
            if all([next(position) for position in position_iterators]):
                return delay

# vim:expandtab:sw=4:ts=4
