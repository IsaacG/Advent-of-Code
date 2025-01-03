#!/bin/python
"""Advent of Code, Day 8: Treetop Tree House. Compute tree visibility."""

import math
from lib import aoc

SAMPLE = [
    """\
30373
25512
65332
33549
35390"""
]


class Day08(aoc.Challenge):
    """Day 8: Treetop Tree House."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=21),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=8),
    ]

    def part1(self, puzzle_input: aoc.Map) -> int:
        """Return how many trees are visible from outside.

        Walk the perimeter and peer into the forest.
        Record how many trees we can see along every line.
        """
        board = puzzle_input.chars

        visible: set[complex] = set()

        edge_location: complex = 0
        walk_direction: complex = 1

        for _ in range(4):
            look_direction = walk_direction * complex(0, 1)
            while True:
                # Look into the forest and record what can be seen.
                viewing = edge_location
                max_height = -1
                while viewing in board:
                    if board[viewing] > max_height:
                        max_height = board[viewing]
                        visible.add(viewing)
                    viewing += look_direction
                # Stop walking before exiting the forest.
                if edge_location + walk_direction not in board:
                    break
                edge_location += walk_direction
            # Rotate 90 degrees.
            walk_direction *= complex(0, 1)

        return len(visible)

    def part2(self, puzzle_input: aoc.Map) -> int:
        """Return the highest scenic score in the forest."""
        board = puzzle_input.chars
        scores = []

        for tree in board:
            # Count how many trees are visible from this one (multiplied).
            # Walk in every direction until the edge of the board or blocked.
            # Count steps. Multiply.
            visible = []
            for direction in aoc.FOUR_DIRECTIONS:
                cur = tree + direction
                num = 0
                while cur in board:
                    num += 1
                    if board[cur] >= board[tree]:
                        break
                    cur += direction
                visible.append(num)
            scores.append(math.prod(visible))

        return max(scores)
