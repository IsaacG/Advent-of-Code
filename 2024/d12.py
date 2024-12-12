#!/bin/python
"""Advent of Code, Day 12: Garden Groups."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

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
        """Walk the edge of a region and count turns."""
        area = len(region)
        if area == 1:
            return 4

        perimeters = 0
        unwalked_walls = {r for r in region if any(n not in region for n in aoc.neighbors(r))}
        while unwalked_walls:
            cur = next(r for r in unwalked_walls if any(n not in region for n in aoc.neighbors(r)))
            unwalked_walls.remove(cur)
            direction = next(d for d in aoc.FOUR_DIRECTIONS if cur + d not in region)
            while cur + direction not in region:
                direction *= -1j
            start_pos = cur
            start_dir = direction

            perimeter = 0
            while cur != start_pos or direction != start_dir or perimeter < 1:
                unwalked_walls.discard(cur)
                if cur + direction * 1j in region:
                    direction *= 1j
                    perimeter += 1
                while cur + direction not in region:
                    direction *= -1j
                    perimeter += 1
                if cur == start_pos and direction == start_dir and perimeter:
                    break
                if cur + direction in region:
                    cur += direction
                    unwalked_walls.discard(cur)
            perimeters += perimeter
        return perimeters

    def solver(self, puzzle_input: aoc.Map, part_one: bool) -> int:
        perimeter = self.perimeter1 if part_one else self.perimeter2
        return sum(len(region) * perimeter(region) for _, region in aoc.partition_regions(puzzle_input.chars))

# vim:expandtab:sw=4:ts=4
