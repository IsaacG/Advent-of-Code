#!/bin/python
"""Advent of Code, Day 18: Like a GIF For Your Yard. Conway's Game of Life."""

from lib import aoc

SAMPLE = """\
.#.#.#
...##.
#....#
..#...
#.#..#
####.."""

InputType = aoc.Board


class Day18(aoc.Challenge):
    """Day 18: Like a GIF For Your Yard."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=4),
        aoc.TestCase(inputs=SAMPLE, part=2, want=17),
    ]

    def simulate(self, bitmap: aoc.Map, cycles: int, corners: bool) -> int:
        """Run Conway's Game of Life and return number of lights on at end."""
        # The number of neighbors which will turn a light on.
        want = {True: (2, 3), False: (3,)}
        # Track just the lights which are on.
        on = bitmap["#"]
        corner_points = bitmap.corners

        for _ in range(cycles):
            if corners:
                on.update(corner_points)
            # Consider cells which are on or adjacent to an on.
            candidates = {
                point + direction
                for point in on
                for direction in aoc.EIGHT_DIRECTIONS
                if point + direction in bitmap
            } | on

            new = set()
            for point in candidates:
                count = sum(point + direction in on for direction in aoc.EIGHT_DIRECTIONS)
                if count in want[point in on]:
                    new.add(point)
            on = new

        if corners:
            on.update(corner_points)
        return len(on)

    def part1(self, puzzle_input: InputType) -> int:
        """Return the number of lights on, with corners not stuck."""
        cycles = 4 if self.testing else 100
        return self.simulate(puzzle_input, cycles, False)

    def part2(self, puzzle_input: InputType) -> int:
        """Return the number of lights on, with corners stuck on."""
        cycles = 5 if self.testing else 100
        return self.simulate(puzzle_input, cycles, True)
