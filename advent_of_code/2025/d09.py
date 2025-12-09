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

        # y, x1, x2
        horizontal_walls = [
            (points[i][1], *sorted([points[i][0], points[i+1][0]]))
            for i in range(0, lines, 2)
        ]
        # x, y1, y2
        vertical_walls = [
            (points[i][0], *sorted([points[i][1], points[i+1][1]]))
            for i in range(1, lines + 1, 2)
        ]

        def valid(rect_x1, rect_y1, rect_x2, rect_y2):
            top, bottom = sorted([rect_y1, rect_y2])
            left, right = sorted([rect_x1, rect_x2])

            for (y, x1, x2) in horizontal_walls:
                if top < y < bottom and x1 < right and x2 > left:
                    return False
            for (x, y1, y2) in vertical_walls:
                if left < x < right and y1 < bottom and y2 > top:
                    return False
            return True

        best = 0
        for (x1, y1), (x2, y2) in itertools.combinations(puzzle_input, 2):
            size = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if size > best and (part_one or valid(x1, y1, x2, y2)):
                best = size
        return best

    def condensed_slower_code(self, puzzle_input: list[list[int]], part_one: bool) -> int:
        """A more compact version of the solution."""
        points = puzzle_input[-1:] + puzzle_input
        walls = [
            (*sorted([x1, x2]), *sorted([y1, y2]))
            for (x1, y1), (x2, y2) in zip(points, points[1:])
        ]

        def valid(x1, y1, x2, y2):
            top, bottom = sorted([y1, y2])
            left, right = sorted([x1, x2])
            return not any(
                y1 < bottom and y2 > top and x1 < right and x2 > left
                for (x1, x2, y1, y2) in walls
            )

        return max(
            (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            for (x1, y1), (x2, y2) in itertools.combinations(puzzle_input, 2)
            if part_one or valid(x1, y1, x2, y2)
        )

# vim:expandtab:sw=4:ts=4
