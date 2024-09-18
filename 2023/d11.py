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
    INPUT_PARSER = aoc.AsciiBoolMapParser("#")
    PARAMETERIZED_INPUTS = [2, 1_000_000]

    def solver(self, parsed_input: InputType, param: bool) -> int:
        """Return the sum of the distances between shifted galaxies."""
        data = parsed_input
        distance = param - 1
        min_x, min_y, max_x, max_y = aoc.bounding_coords(data)

        # Compute the shift for each column and row.
        offset_columns = []
        offset = 0
        for x in range(min_x, max_x + 1):
            if not any(pos.real == x for pos in data):
                offset += distance
            offset_columns.append(offset)

        offset_rows = []
        offset = 0
        for y in range(min_y, max_y + 1):
            if not any(pos.imag == y for pos in data):
                offset += distance
            offset_rows.append(offset)

        # Shift all galaxies.
        data = {
            pos + complex(offset_columns[int(pos.real)], offset_rows[int(pos.imag)])
            for pos in data
        }

        return int(
            sum(
                abs(b.real - a.real) + abs(b.imag - a.imag)
                for a, b in itertools.combinations(data, 2)
            )
        )

# vim:expandtab:sw=4:ts=4
