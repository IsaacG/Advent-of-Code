#!/bin/python
"""Advent of Code, Day 18: Like a GIF For Your Yard. Conway's Game of Life."""

import typer
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
    INPUT_PARSER = aoc.ParseCharMap(lambda x: x == "#")

    def solver(self, bitmap: dict[complex, bool], cycles: int, corners: bool) -> int:
        """Run Conway's Game of Life and return number of lights on at end."""
        # The number of neighbors which will turn a light on.
        want = {True: (2, 3), False: (3,)}
        # Track just the lights which are on.
        on = {p for p, v in bitmap.items() if v}
        corner_points = aoc.Board(bitmap).corners

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

    def part1(self, parsed_input: InputType) -> int:
        """Return the number of lights on, with corners not stuck."""
        cycles = 4 if self.testing else 100
        return self.solver(parsed_input, cycles, False)

    def part2(self, parsed_input: InputType) -> int:
        """Return the number of lights on, with corners stuck on."""
        cycles = 5 if self.testing else 100
        return self.solver(parsed_input, cycles, True)


if __name__ == "__main__":
    typer.run(Day18().run)

# vim:expandtab:sw=4:ts=4
