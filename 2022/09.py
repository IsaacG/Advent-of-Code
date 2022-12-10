#!/bin/python
"""Advent of Code, Day 9: Rope Bridge. Track the movement of knots."""

import typer
from lib import aoc

SAMPLE = [
    """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""",
    """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""",
]

LineType = tuple[str, int]
InputType = list[LineType]


class Day09(aoc.Challenge):
    """Day 9: Rope Bridge."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=13),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=36),
    ]
    INPUT_PARSER = aoc.parse_multi_mixed_per_line

    def solver(self, lines: list[tuple[str, int]], knot_count: int) -> int:
        """Track the movement of knots on a rope. Return the number of positions the tail visits."""
        points: set[complex] = set([0])
        knots: list[complex] = [0] * knot_count
        movement = {"R": 1, "L": -1, "U": 1j, "D": -1j}
        for direction, unit in lines:
            for _ in range(unit):
                knots[0] += movement[direction]
                for i, (a, b) in enumerate(zip(knots, knots[1:])):
                    if a - b in aoc.NEIGHBORS:
                        continue
                    x = self.cmp(a.real, b.real)
                    y = self.cmp(a.imag, b.imag)
                    knots[i + 1] += complex(x, y)
                points.add(knots[-1])
        return len(points)

    def part1(self, parsed_input: InputType) -> int:
        """Return visited locations for a 2-knot rope tail."""
        return self.solver(parsed_input, 2)

    def part2(self, parsed_input: InputType) -> int:
        """Return visited locations for a 10-knot rope tail."""
        return self.solver(parsed_input, 10)


if __name__ == "__main__":
    typer.run(Day09().run)

# vim:expandtab:sw=4:ts=4
