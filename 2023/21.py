#!/bin/python
"""Advent of Code, Day 21: Step Counter."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

InputType = tuple[set[complex], set[complex], set[complex]]


class Day21(aoc.Challenge):
    """Day 21: Step Counter."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=16),
        aoc.TestCase(inputs=SAMPLE, part=2, want=1),
    ]

    def walk(self, start, garden, rocks, steps):
        reach = start
        min_x, min_y, max_x, max_y = aoc.bounding_coords(garden)
        max_x += 1
        max_y += 1
        for s in range(steps):
            new = set()
            for p in reach:
                for n in aoc.neighbors(p):
                    if complex(n.real % max_x, n.imag % max_y) not in rocks:
                        new.add(n)
            reach = new
        return reach

    def part1(self, parsed_input: InputType) -> int:
        start, garden, _ = parsed_input
        steps = 64
        if self.testing:
            steps = 6

        reach = start.copy()
        for s in range(steps):
            n = set()
            for p in reach:
                n.update(aoc.neighbors(p))
            reach = n & garden
        return len(reach)

    def test_p2(self, parsed_input: InputType) -> int:
        steps_count = [(6, 16), (10, 50), (50, 1594), (100, 6536)]

        start, garden, rocks = parsed_input
        for steps, want in steps_count:
            got = len(self.walk(start, garden, rocks, steps))
            assert got == want, f"{(steps, want, got)=}"

    def part2(self, parsed_input: InputType) -> int:
        if self.testing:
            self.test_p2(parsed_input)
            return 1
        start, garden, rocks = parsed_input
        steps = 26501365

        min_x, min_y, max_x, max_y = aoc.bounding_coords(garden)
        size = max_x - min_x + 1
        half_size = max_x // 2
        expansions = (steps - half_size) // size

        # Explore the garden for 2 garden lengths to compute garden values.
        # Those garden values are then used to multiply and compute the expanded version
        # since they expand in a reliable pattern.
        manual_expansions = 2
        reach = self.walk(start, garden, rocks, half_size + manual_expansions * size)

        rows = []
        for y in range(-manual_expansions, manual_expansions + 1):
            row = []
            top = size * y
            bottom = top + size
            for x in range(-manual_expansions, manual_expansions + 1):
                left = size * x
                right = left + size
                num = len({p for p in reach if left <= p.real < right and top <= p.imag < bottom})
                row.append(num)
            rows.append(row)
            self.debug(" | ".join(f"{r:5}" for r in row))
        self.debug("")

        # The pointy tips. Top/bottom center and extreme right/right.
        tips = rows[0][2] + rows[-1][2] + rows[2][0] + rows[2][-1]
        # The edges have two types of gardens: 1/4 filled and 3/4 filled.
        short_diag = rows[0][1] + rows[0][3] + rows[-1][1] + rows[-1][3]
        large_diag = rows[1][1] + rows[1][3] + rows[3][1] + rows[3][3]
        # Interior gardens alternate.
        interior_center = rows[2][2]
        interior_even = rows[2][1]

        return (
            tips
            + expansions * short_diag
            + (expansions - 1) * large_diag
            + interior_center * (expansions - 1) ** 2
            + interior_even * expansions ** 2
        )


    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        start = aoc.parse_ascii_bool_map("S").parse(puzzle_input)
        garden = aoc.parse_ascii_bool_map(".").parse(puzzle_input) | start
        rocks = aoc.parse_ascii_bool_map("#").parse(puzzle_input)
        return start, garden, rocks

# vim:expandtab:sw=4:ts=4
