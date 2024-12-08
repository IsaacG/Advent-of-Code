#!/bin/python
"""Advent of Code, Title."""

import itertools
from lib import aoc

SAMPLE = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""


class Day08(aoc.Challenge):
    """Title."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=14),
        aoc.TestCase(part=2, inputs=SAMPLE, want=34),
    ]
    INPUT_PARSER = aoc.CoordinatesParser()

    def solver(self, puzzle_input: dict[str, set[complex]], part_one: bool) -> int:
        all_locations = puzzle_input.all_coords
        antinodes = set()
        for freq in puzzle_input.non_blank_chars:
            for a, b in itertools.combinations(puzzle_input.coords[freq], 2):
                if part_one:
                    sequences = ([2], [-1])
                else:
                    sequences = (itertools.count(), itertools.count(step=-1))

                delta = b - a
                for steps in sequences:
                    for i in steps:
                        if (node := a + i * delta) in all_locations:
                            antinodes.add(node)
                        else:
                            break

        return len(antinodes)

# vim:expandtab:sw=4:ts=4
