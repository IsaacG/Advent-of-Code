#!/bin/python
"""Advent of Code: Day 20."""

import functools
import typer
from lib import aoc
import input_data

SAMPLE = input_data.D20_SAMPLE
InputType = tuple[dict[str, bool], set[complex]]


class Day20(aoc.Challenge):
    """Image enhancing algorithm."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=35),
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=1),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=3351),
    )

    def part1(self, parsed_input: InputType) -> int:
        """Enhance the image twice and return pixels enabled."""
        return self.enhance(parsed_input, 2)

    def part2(self, parsed_input: InputType) -> int:
        """Enhance the image 50 times and return pixels enabled."""
        return self.enhance(parsed_input, 50)

    @staticmethod
    @functools.cache  # 2x faster
    def point_to_area(point: complex):
        """Return the 3x3 points centered around `point`."""
        return [point + complex(x, y) for y in range(-1, 2) for x in range(-1, 2)]

    def enhance(self, parsed_input: InputType, steps: int) -> int:
        """Enhance the image N times.

        For every iteration, expand the area of interest by expanding outwards
        one step from the prior iteration. For all points in that area,
        examine all their neighbors to determine their new state.

        When blinking is in effect, points outside the area of interest (from
        the prior iteration) are "unexplored" and blink on and off.

        When they blink off, they can be ignored. When blinked on (even steps),
        any point outside the "explored" region are "on" when evaluated.
        """
        algo, image = parsed_input

        # The background blinks if 000_000_000 => on and 111_111_111 => off
        is_blinking = algo["000" * 3] and not algo["111" * 3]
        # Mapping to translate bool to str to a binary number.
        trans = {True: "1", False: "0"}

        candidate_points = image
        new_area = image

        for step in range(steps):
            # The explored area is the points we evaluated last iteration.
            # Anything not explored may be blinking.
            explored = candidate_points
            # Expand the area of interest by one neighbor.
            # We could use the old candidate_points directly to compute the new
            # candidate_points, but tracking what area is "new" reduces the area
            # which needs expanding and speeds things up.
            # candidate_points = set().union(*(set(self.point_to_area(point)) for point in candidate_points))
            new_area = set().union(*(set(self.point_to_area(point)) for point in new_area)) - explored
            candidate_points = candidate_points | new_area

            # When the unexplored area is blinked on, points outside the explored
            # area are "on".
            if is_blinking and step % 2:
                on_logic = lambda point: point not in explored or point in image
            else:
                on_logic = lambda point: point in image

            # We could use a tuple(bool, ...) instead of converting to a string
            # but that only saves 10% speed
            def bitstring(point):
                return "".join(trans[on_logic(p)] for p in self.point_to_area(point))

            image = set(
                point
                for point in candidate_points
                if algo[bitstring(point)]
            )

        return len(image)

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        first, second = puzzle_input.split("\n\n")
        algo = {f"{i:09b}": char == "#" for i, char in enumerate(first)}

        image = set(
            complex(x, y)
            for y, line in enumerate(second.splitlines())
            for x, elem in enumerate(line)
            if elem == "#"
        )
        return algo, image


if __name__ == "__main__":
    typer.run(Day20().run)

# vim:expandtab:sw=4:ts=4
