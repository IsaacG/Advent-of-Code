#!/bin/python
"""Advent of Code, Day 18: Lavaduct Lagoon."""

import more_itertools
from lib import aoc

LETTER_DIRECTIONS = {"R": aoc.RIGHT, "L": aoc.LEFT, "U": aoc.UP, "D": aoc.DOWN}
NUM_TO_LETTER = {"0": "R", "2": "L", "3": "U", "1": "D"}

SAMPLE = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""


class Day18(aoc.Challenge):
    """Day 18: Lavaduct Lagoon."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=62),
        aoc.TestCase(inputs=SAMPLE, part=2, want=952408144115),
    ]
    INPUT_PARSER = aoc.parse_multi_str_per_line
    PARAMETERIZED_INPUTS = [False, True]

    def solver(self, parsed_input: list[list[str]], param: bool) -> int:
        position = complex(0)
        vertical_trenches = set()
        prior_direction = complex(0)
        perimeter_size = 0
        # Follow the instructions to compute all the perimeter lines.
        for direction_letter, distance_str, color in parsed_input:
            if param:
                color = color.strip("()#")
                distance = int(color[:-1], 16)
                direction_letter = NUM_TO_LETTER[color[-1]]
            else:
                distance = int(distance_str)
            direction = LETTER_DIRECTIONS[direction_letter]

            # The perimeter_size logic requires we never double back.
            # Assert we always rotate 90 degrees each line.
            assert prior_direction not in (direction, -direction)
            prior_direction = direction

            start = position
            end = position + direction * distance
            perimeter_size += distance
            position = end

            # Record vertical trenches, but sorted.
            if direction in (aoc.UP, aoc.DOWN):
                if start.imag > end.imag:
                    start, end = end, start
                vertical_trenches.add((start, end))

        assert position == complex(0)

        count = 0
        # Split the map into segments split at y-values where trenches start/end.
        y_points = sorted({int(p.imag) for points in vertical_trenches for p in points})
        for start_y, end_y in zip(y_points, y_points[1:]):
            # For each y-range, find the trenches which exist across that range.
            open_ranges = [
                int(start.real) for (start, end) in vertical_trenches
                if start.imag <= start_y and end_y <= end.imag
            ]
            # Pair those trenches into open-close pairs and compute the area.
            open_ranges.sort()
            for start_x, end_x in more_itertools.chunked(open_ranges, 2):
                block_size = (end_x - start_x) * (end_y - start_y)
                count += block_size

        # The block-area includes one edge but not the other.
        # This makes overlapping blocks work. But requires we add on the perimeter after.
        return count + (perimeter_size // 2) + 1


# vim:expandtab:sw=4:ts=4
