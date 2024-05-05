#!/bin/python
"""Advent of Code, Day 12: Hill Climbing Algorithm. Solve for the shortest path through a maze."""

import string
import collections

from lib import aoc

SAMPLE = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

InputType = tuple[complex, complex, aoc.Board]


class Day12(aoc.Challenge):
    """Day 12: Hill Climbing Algorithm."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=31),
        aoc.TestCase(inputs=SAMPLE, part=2, want=29),
    ]

    def get_steps(self, starts: list[complex], end: complex, board: aoc.Board) -> int:
        """Return the min steps from start to end."""
        step_count = {point: 0 for point in starts}
        to_visit = collections.deque(starts)

        while to_visit:
            point = to_visit.popleft()
            for neighbor, height in board.neighbors(point).items():
                # Cannot climb a steep hill.
                if height - 1 > board[point]:
                    continue
                if neighbor in step_count:
                    continue
                if neighbor == end:
                    return step_count[point] + 1
                step_count[neighbor] = step_count[point] + 1
                to_visit.append(neighbor)
        raise RuntimeError("Not found.")

    def part1(self, parsed_input: InputType) -> int:
        """Return steps from start to end."""
        start, end, board = parsed_input
        return self.get_steps([start], end, board)

    def part2(self, parsed_input: InputType) -> int:
        """Return steps from any low point to end."""
        _, end, board = parsed_input
        starts = [
            point
            for point, height in board.items()
            if height == 0
        ]
        return self.get_steps(starts, end, board)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        heights = {}
        start, end = None, None
        for y, row in enumerate(puzzle_input.splitlines()):
            for x, char in enumerate(row):
                if char == "S":
                    start = complex(x, y)
                    char = "a"
                if char == "E":
                    end = complex(x, y)
                    char = "z"
                heights[complex(x, y)] = string.ascii_lowercase.index(char)

        if start is None or end is None:
            raise ValueError("Failed to find start and end.")
        return start, end, aoc.Board(heights, diagonal=False)
