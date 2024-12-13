#!/bin/python
"""Advent of Code: Day 09."""

import math
from lib import aoc

SAMPLE = ["""\
2199943210
3987894921
9856789892
8767896789
9899965678
"""]


class Day09(aoc.Challenge):
    """Find low points and basins in a topographic map."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=15),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=1134),
    )
    INPUT_PARSER = aoc.CoordinatesParser()

    @classmethod
    def lows(cls, depths: aoc.Map) -> list[complex]:
        """Return all the minimum points on the map."""
        return [
            point
            for point, depth in depths.items()
            if all(
                depth < depths.get(n, 10) for n in aoc.neighbors(point)
            )
        ]

    def part1(self, puzzle_input: aoc.Map) -> int:
        """Find all the low points on the map."""
        depths = puzzle_input
        return sum(depths[point] + 1 for point in self.lows(puzzle_input.chars))

    def part2(self, puzzle_input: aoc.Map) -> int:
        """Find the largest three basins.

        Simply remove 9's from the map and find the size of each island."""
        # Remove borders around the islands, i.e. points of height 9.
        unexplored = {point for point, depth in puzzle_input.chars.items() if depth != 9}
        basins = aoc.partition_regions(unexplored, predicate=lambda a, b: True)
        basin_sizes = (len(basin) for basin in basins)

        return math.prod(sorted(basin_sizes, reverse=True)[:3])
