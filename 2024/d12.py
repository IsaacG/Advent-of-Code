#!/bin/python
"""Advent of Code, Day 12: Garden Groups."""

from lib import aoc

SAMPLE = [
    """\
AAAA
BBCD
BBCC
EEEC""",  # 0
    """\
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO""",  # 1
    """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""",  # 2
    """\
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE""",  # 3
    """\
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""  # 4
]


class Day12(aoc.Challenge):
    """Day 12: Garden Groups."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=140),  # 1
        aoc.TestCase(part=1, inputs=SAMPLE[1], want=772),  # 2
        aoc.TestCase(part=1, inputs=SAMPLE[2], want=1930), # 3
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=80),   # 4
        aoc.TestCase(part=2, inputs=SAMPLE[3], want=236),  # 5
        aoc.TestCase(part=2, inputs=SAMPLE[4], want=368),  # 6
        aoc.TestCase(part=2, inputs=SAMPLE[2], want=1206), # 7
    ]

    def perimeter1(self, region: set[complex]) -> int:
        """Count the number of edges which borders the edge of the region."""
        return sum(
            1
            for cur in region
            for n in aoc.neighbors(cur)
            if n not in region
        )

    def perimeter2(self, region: set[complex]) -> int:
        """Count the number of edge-runs.

        This can be computed by counting the number of "corners" a region has.
        A point is a convex corner if it no neighbors in two adjacent directions (eg up and right).
        A point is a concave corner if there are neighbors in
        two adjacent directions (eg up and right) but not diagonal in those directions.
        """
        d1, d2, d3 = complex(1, 0), complex(0, 1), complex(1, 1)
        convex_corners = sum(
            1
            for coord in region
            for rotation in aoc.FOUR_DIRECTIONS
            if coord + d1 * rotation not in region and coord + d2 * rotation not in region
        )
        concave_corners = sum(
            1
            for coord in region
            for rotation in aoc.FOUR_DIRECTIONS
            if (
                coord + d1 * rotation in region
                and coord + d2 * rotation in region
                and coord + d3 * rotation not in region
            )
        )
        return convex_corners + concave_corners

    def solver(self, puzzle_input: aoc.Map, part_one: bool) -> int:
        perimeter = self.perimeter1 if part_one else self.perimeter2
        return sum(
            len(region) * perimeter(region)
            for _, region in aoc.partition_regions(puzzle_input.chars)
        )

# vim:expandtab:sw=4:ts=4
