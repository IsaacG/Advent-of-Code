#!/bin/python
"""Advent of Code, Day 12: Garden Groups."""
from lib import aoc


def perimeter1(region: set[complex]) -> int:
    """Count the number of edges which borders the edge of the region."""
    return sum(
        1
        for cur in region
        for n in aoc.neighbors(cur)
        if n not in region
    )


def perimeter2(region: set[complex]) -> int:
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


def solve(data: aoc.Map, part: int) -> int:
    perimeter = perimeter1 if part == 1 else perimeter2
    garden = {complex(*p): v for p, v in data.chars.items()}
    return sum(
        len(region) * perimeter(region)
        for region in aoc.partition_regions(
            garden, predicate=lambda a, b: garden[a] == garden[b]
        )
    )


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
TESTS = [
    (1, SAMPLE[0], 140),  # 1
    (1, SAMPLE[1], 772),  # 2
    (1, SAMPLE[2], 1930), # 3
    (2, SAMPLE[0], 80),   # 4
    (2, SAMPLE[3], 236),  # 5
    (2, SAMPLE[4], 368),  # 6
    (2, SAMPLE[2], 1206), # 7
]
# vim:expandtab:sw=4:ts=4
