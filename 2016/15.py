#!/bin/python
"""Advent of Code, Day 15: Timing is Everything. Determine when a hole in disks line up."""

import itertools
from lib import aoc

SAMPLE = """\
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1."""

InputType = list[list[int]]


class Day15(aoc.Challenge):
    """Day 15: Timing is Everything."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=5),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        """Return the correct time to press the button to get a capsule."""
        disks = [
            (number + start, positions)
            for number, positions, _, start in parsed_input
        ]
        return next(
            time
            for time in itertools.count()
            if all(((start + time) % positions) == 0 for start, positions in disks)
        )

    def part2(self, parsed_input: InputType) -> int:
        """Solve with an additional disk."""
        new_disk = [parsed_input[-1][0] + 1, 11, 0, 0]
        return self.part1(parsed_input + [new_disk])
