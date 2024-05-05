#!/bin/python
"""Advent of Code, Day 18: Lavaduct Lagoon."""

import collections
import more_itertools
from lib import aoc

LETTER_DIRECTIONS = aoc.LETTER_DIRECTIONS
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
        # Start at 0, 0 and track vertical trenches.
        position = complex(0)
        vertical_trenches = set()
        prior_direction = complex(0)
        perimeter_size = 0
        # Follow the instructions to compute all the perimeter lines.
        for direction_letter, distance_str, color in parsed_input:
            if param:
                # Part two: read the instructions out of the color label.
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

        # To close the loop, we need to end where we started.
        assert position == complex(0)

        # Do vertical and horizontal line scanning.
        # The starts and ends are the trenches ordered of
        # when they need to be applied in a single pass.
        starts = collections.deque(sorted(
            (line for line in vertical_trenches),
            key=lambda x: x[0].imag
        ))
        ends = collections.deque(sorted(
            (line for line in vertical_trenches),
            key=lambda x: x[1].imag
        ))
        active: list[tuple[complex, complex]] = []

        start_y = starts[0][0].imag
        count = 0.0
        while ends:
            # Find where the next change happens, either due to a new start or an end.
            end_y = ends[0][1].imag
            if starts:
                end_y = min(end_y, starts[0][0].imag)
            # Sort active trenches left to right then iterate in open/close pairs.
            # The area between the trenches is a block of open pit to add.
            active.sort(key=lambda x: x[0].real)
            for start_line, end_line in more_itertools.chunked(active, 2):
                start_x, end_x = start_line[0].real, end_line[0].real
                block_size = (end_x - start_x) * (end_y - start_y)
                count += block_size

            # Update the active ranges. The end_y is where there are new starts/ends to apply.
            # Use starts to add new active trenches and ends are used
            # to remove trenches when we hit the bottom.
            start_y = end_y
            while starts and starts[0][0].imag == start_y:
                active.append(starts.popleft())
            while ends and ends[0][1].imag == start_y:
                active.remove(ends.popleft())
        # The block-area includes one edge but not the other.
        # This makes overlapping blocks work. But requires we add on the perimeter after.
        count += (perimeter_size // 2) + 1
        return int(count)


# vim:expandtab:sw=4:ts=4
