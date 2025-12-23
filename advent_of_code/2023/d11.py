#!/bin/python
"""Advent of Code, Day 11: Cosmic Expansion."""

import itertools

from lib import aoc

InputType = set[complex]
SAMPLE = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


class Day11(aoc.Challenge):
    """Day 11: Cosmic Expansion."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=374),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]

    def solver(self, puzzle_input: InputType, part_one: bool) -> int:
        """Return the sum of the distances between shifted galaxies."""
        data = puzzle_input.coords["#"]
        distance = 1 if part_one else 1_000_000 - 1
        min_x, min_y = min(d[0] for d in data), min(d[1] for d in data)
        max_x, max_y = max(d[0] for d in data), max(d[1] for d in data)

        # Compute the shift for each column and row.
        offset_columns = []
        offset = 0
        for x in range(min_x, max_x + 1):
            if not any(pos[0] == x for pos in data):
                offset += distance
            offset_columns.append(offset)

        offset_rows = []
        offset = 0
        for y in range(min_y, max_y + 1):
            if not any(pos[1] == y for pos in data):
                offset += distance
            offset_rows.append(offset)

        # Shift all galaxies.
        data = {
            (pos[0] + offset_columns[pos[0]], pos[1] + offset_rows[pos[1]])
            for pos in data
        }

        return int(
            sum(
                abs(b[0] - a[0]) + abs(b[1] - a[1])
                for a, b in itertools.combinations(data, 2)
            )
        )

# vim:expandtab:sw=4:ts=4
