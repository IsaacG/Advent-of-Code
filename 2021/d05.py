#!/bin/python

"""Advent of Code: Day 05."""

import collections
import itertools
import re

from lib import aoc

SAMPLE = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""

# A list of point->point pairs, delineating a line.
InputType = list[aoc.Line]


class Day05(aoc.Challenge):
    """Map where geothermal vent clouds cross paths."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=5),
        aoc.TestCase(inputs=SAMPLE, part=2, want=12),
    )

    def part1(self, puzzle_input: InputType) -> int:
        """Find hot areas where lines overlap. Ignore diagonals."""
        # Filter for horizontal/vertical and call part 2.
        puzzle_input = [line for line in puzzle_input if line.start.x == line.end.x or line.start.y == line.end.y]
        return self.part2(puzzle_input)

    def part2(self, puzzle_input: InputType) -> int:
        """Find hot areas where puzzle_input overlap. Include diagonals."""
        # Count points that are on lines.
        count = collections.Counter(
            itertools.chain.from_iterable(line.points() for line in puzzle_input)
        )
        return sum(1 for v in count.values() if v > 1)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data.

        Split into lines. Split each line into a `start -> end`.
        Make a tuple(begin, end) Points for each line.
        """
        pattern = re.compile(r'^([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)$')
        lines = []
        for line in puzzle_input.splitlines():
            match = pattern.match(line)
            lines.append(
                aoc.Line(
                    aoc.Point(int(match.group(1)), int(match.group(2))),
                    aoc.Point(int(match.group(3)), int(match.group(4))),
                )
            )
        return lines
