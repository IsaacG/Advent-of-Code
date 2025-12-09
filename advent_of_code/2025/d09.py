#!/bin/python
"""Advent of Code, Day 9: Movie Theater."""
import itertools

from lib import aoc

SAMPLE = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""


class Day09(aoc.Challenge):
    """Day 9: Movie Theater."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=50),
        aoc.TestCase(part=2, inputs=SAMPLE, want=24),
    ]

    def solver(self, puzzle_input: list[list[int]], part_one: bool) -> int:
        if puzzle_input[0][0] == puzzle_input[1][0]:
            points = puzzle_input[-1:] + puzzle_input
        else:
            points = puzzle_input + puzzle_input[:1]

        lines = len(puzzle_input)

        # Horizontal (y, x1, x2) and vertical walls (x, y1, y2).
        horiz_and_vert_walls = [
            [
                (points[i][1 - direction], *sorted([points[i][direction], points[i + 1][direction]]))
                for i in range(direction, lines + direction, 2)
            ]
            for direction in [0, 1]
        ]

        def valid(x1, y1, x2, y2):
            top, bottom = sorted([y1, y2])
            left, right = sorted([x1, x2])

            for i, walls in enumerate(horiz_and_vert_walls):
                if i:
                    top, bottom, left, right = left, right, top, bottom
                for (y, x1, x2) in walls:
                    if top < y < bottom and x1 < right and x2 > left:
                        return False
            return True

        best = 0
        for (x1, y1), (x2, y2) in itertools.combinations(puzzle_input, 2):
            size = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if size > best and (part_one or valid(x1, y1, x2, y2)):
                best = size
        return best

# vim:expandtab:sw=4:ts=4
