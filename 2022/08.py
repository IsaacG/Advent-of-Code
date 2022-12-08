#!/bin/python
"""Advent of Code, Day 8: Treetop Tree House. Compute tree visibility."""

import typer
from lib import aoc

SAMPLE = [
    """\
30373
25512
65332
33549
35390"""
]

InputType = aoc.Board


class Day08(aoc.Challenge):
    """Day 8: Treetop Tree House."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=21),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=8),
    ]

    def part1(self, parsed_input: InputType) -> int:
        """Return how many trees are visible from outside."""
        board = parsed_input
        count = 0

        for tree in board:
            # Check if a tree is visible.
            # Pick a direction. Walk in that direction until blocked or reach the edge.
            # If we get to the edge, the tree is visible.
            for direction in aoc.DIRECTIONS:
                cur = tree + direction
                while cur in board:
                    if board[cur] >= board[tree]:
                        break
                    cur += direction
                else:
                    # Loop exited, got out to the edge.
                    count += 1
                    break

        return count

    def part2(self, parsed_input: InputType) -> int:
        """Return the highest scenic score in the forest."""
        board = parsed_input
        scores = []

        for tree in board:
            # Count how many trees are visible from this one (multiplied).
            # Walk in every direction until the edge of the board or blocked.
            # Count steps. Multiply.
            visible = []
            for direction in aoc.DIRECTIONS:
                cur = tree + direction
                num = 0
                while cur in board:
                    num += 1
                    if board[cur] >= board[tree]:
                        break
                    cur += direction
                visible.append(num)
            scores.append(self.mult(visible))

        return max(scores)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return aoc.Board.from_int_block(puzzle_input)


if __name__ == "__main__":
    typer.run(Day08().run)

# vim:expandtab:sw=4:ts=4
