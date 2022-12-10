#!/bin/python
"""Advent of Code: Day 04."""

import typer
from lib import aoc

SAMPLE = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
InputType = list[list[int]]


class Day04(aoc.Challenge):
    """Day 4: Camp Cleanup. Detect overlapping ranges."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=2),
        aoc.TestCase(inputs=SAMPLE, part=2, want=4),
    ]
    INPUT_PARSER = aoc.parse_re_findall_int(r"\d+")

    def part1(self, parsed_input: InputType) -> int:
        """Return the number of fully contained overlaps."""
        return sum(
            True
            for a1, a2, b1, b2 in parsed_input
            if (a1 >= b1 and a2 <= b2) or (b1 >= a1 and b2 <= a2)
        )

    def part2(self, parsed_input: InputType) -> int:
        """Return the number of partial overlaps."""
        return sum(
            True
            for a1, a2, b1, b2 in parsed_input
            if b1 <= a1 <= b2 or a1 <= b1 <= a2
        )


if __name__ == "__main__":
    typer.run(Day04().run)

# vim:expandtab:sw=4:ts=4
