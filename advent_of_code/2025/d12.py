#!/bin/python
"""Advent of Code, Day 12: Christmas Tree Farm."""

from lib import aoc

SAMPLE = """\
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""

InputType = tuple[list[set[complex]], tuple[int, int, list[int]]]

class Day12(aoc.Challenge):
    """Day 12: Christmas Tree Farm."""

    TESTS = [
        # Only one part. The "trick" with the actual input doesn't apply to the example.
        # aoc.TestCase(part=1, inputs=SAMPLE[0], want=2),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    def solver(self, puzzle_input: InputType, part_one: bool) -> int:
        shapes, areas = puzzle_input
        sizes = [len(i) for i in shapes]

        # orientations = [all_orients(shape) for shape in shapes]

        def can_fit(x, y, wants):
            if sum(num * sizes[idx] for idx, num in enumerate(wants)) > x * y:
                return False
            if x * y >= 9 * sum(wants):
                return True
            return False

        return sum(can_fit(*area) for area in areas)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        *shapes_, areas_ = puzzle_input.split("\n\n")
        shapes = [
            {
                complex(x, y)
                for y, line in enumerate(shape.splitlines()[1:])
                for x, char in enumerate(line)
                if char == "#"
            }
            for shape in shapes_
        ]
        areas = []
        for line in areas_.splitlines():
            x, y, *wants = aoc.parse_ints_one_line.parse(line)
            areas.append((x, y, wants))
        return shapes, areas

# vim:expandtab:sw=4:ts=4
