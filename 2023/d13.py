#!/bin/python
"""Advent of Code, Day 13: Point of Incidence."""

from lib import aoc

SAMPLE = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

InputType = list[set[complex]]


class Day13(aoc.Challenge):
    """Day 13: Point of Incidence."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=405),
        aoc.TestCase(inputs=SAMPLE, part=2, want=400),
    ]
    INPUT_PARSER = aoc.ParseBlocks([aoc.AsciiBoolMapParser("#")])

    def find_mirror(self, points: set[complex], point: complex | None) -> int | None:
        """Find the row/column around which the data is mirrored.

        Optionally take a point which must be reflected.
        """
        min_x, min_y, max_x, max_y = aoc.bounding_coords(points)

        for x in range(min_x, max_x):
            shift = 2 * x + 1
            if point is not None and not min_x <= shift - point.real <= max_x:
                continue
            if all(complex(shift - p.real, p.imag) in points for p in points if min_x <= shift - p.real <= max_x):
                return x + 1

        for y in range(min_y, max_y):
            shift = 2 * y + 1
            if point is not None and not min_y <= shift - point.imag <= max_y:
                continue
            if all(complex(p.real, shift - p.imag) in points for p in points if min_y <= shift - p.imag <= max_y):
                return 100 * (y + 1)

        return None

    def find_with_change(self, points: set[complex]) -> int:
        """Try finding the mirror with a point toggled."""
        points = points.copy()
        min_x, min_y, max_x, max_y = aoc.bounding_coords(points)
        ops = {True: [points.remove, points.add], False: [points.add, points.remove]}
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                point = complex(x, y)
                op_a, op_b = ops[point in points]
                # Add/compute/remove or remove/compute/add.
                op_a(point)
                mirror = self.find_mirror(points, point)
                op_b(point)
                if mirror:
                    return mirror
        raise RuntimeError("Unsolved")

    def part1(self, parsed_input: InputType) -> int:
        return sum(self.find_mirror(points, None) for points in parsed_input)

    def part2(self, parsed_input: InputType) -> int:
        return sum(self.find_with_change(points) for points in parsed_input)

# vim:expandtab:sw=4:ts=4
