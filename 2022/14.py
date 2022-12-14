#!/bin/python
"""Advent of Code, Day 14: Regolith Reservoir. Count how many grains fit in a reservoir."""

import itertools

import typer
from lib import aoc

SAMPLE = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

LineType = list[complex]
InputType = list[LineType]


class Day14(aoc.Challenge):
    """Day 14: Regolith Reservoir."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=24),
        aoc.TestCase(inputs=SAMPLE, part=2, want=93),
    ]
    INPUT_PARSER = aoc.parse_re_findall_points

    def solver(self, rocks: InputType, first_to_the_floor: bool) -> int:
        """Simulate sand filling a reservoir. Return which grain passes the floor or stops falling."""
        # Sand moves in these directions, in this order of preference.
        movement_directions = (complex(0, 1), complex(-1, 1), complex(1, 1))
        starting_point = complex(500, 0)

        # Use the input to build a set of rock points and compute the lowest points.
        rocks_and_sand = set()
        lowest_rock = 0
        for points in rocks:
            lowest_rock = max(lowest_rock, max(p.imag for p in points))
            for start, end in zip(points[:-1], points[1:]):
                for point in aoc.Line.from_complex(start, end).points():
                    rocks_and_sand.add(complex(point))
        # The lowest position a grain may occupy.
        lowest_position = lowest_rock + 1

        # Simulate the grains.
        for grain in itertools.count():
            cur = starting_point
            # Grains can drop until they hit the lowest_position.
            while cur.imag < lowest_position:
                for d in movement_directions:
                    if cur + d not in rocks_and_sand:
                        cur += d
                        break
                else:
                    break
            rocks_and_sand.add(cur)
            if first_to_the_floor and cur.imag == lowest_position:
                # Part 1: return the grain prior to the first to pass the lowest rock.
                return grain
            elif cur == starting_point:
                # Part 2: return the grain which stops at the starting_point.
                return grain + 1

    def part1(self, parsed_input: InputType) -> int:
        """Return the last grain to rest on the lowest rock."""
        return self.solver(parsed_input, True)

    def part2(self, parsed_input: InputType) -> int:
        """Return the grain which stops at the starting_point."""
        return self.solver(parsed_input, False)


if __name__ == "__main__":
    typer.run(Day14().run)

# vim:expandtab:sw=4:ts=4
