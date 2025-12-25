#!/bin/python
"""Advent of Code, Day 9: Rope Bridge. Track the movement of knots."""
from lib import aoc


def solve(data: list[tuple[str, int]], part: int) -> int:
    """Track the movement of knots on a rope. Return the number of positions the tail visits."""
    points: set[complex] = set([0])
    knots: list[complex] = [0] * (2 if part == 1 else 10)
    movement = aoc.LETTER_DIRECTIONS
    for direction, unit in data:
        for _ in range(unit):
            knots[0] += movement[direction]
            for i, (a, b) in enumerate(zip(knots, knots[1:])):
                if a - b in aoc.EIGHT_DIRECTIONS:
                    continue
                x = aoc.cmp(a.real, b.real)
                y = aoc.cmp(a.imag, b.imag)
                knots[i + 1] += complex(x, y)
            points.add(knots[-1])
    return len(points)


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
TESTS = [(1, SAMPLE[0], 13), (2, SAMPLE[1], 36)]
