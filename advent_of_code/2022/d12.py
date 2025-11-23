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

InputType = tuple[complex, complex, dict[complex, int]]


class Day12(aoc.Challenge):
    """Day 12: Hill Climbing Algorithm."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=31),
        aoc.TestCase(inputs=SAMPLE, part=2, want=29),
    ]

    def get_steps(self, starts: list[complex], end: complex, board: dict[complex, int]) -> int:
        """Return the min steps from start to end."""
        step_count = {point: 0 for point in starts}
        to_visit = collections.deque([(p, 0) for p in starts])

        while to_visit:
            point, height = to_visit.popleft()
            for neighbor in aoc.neighbors(point):
                n_height = board.get(neighbor, 99)
                # Cannot climb a steep hill.
                if n_height - 1 > height:
                    continue
                if neighbor in step_count:
                    continue
                if neighbor == end:
                    return step_count[point] + 1
                step_count[neighbor] = step_count[point] + 1
                to_visit.append((neighbor, n_height))
        raise RuntimeError("Not found.")

    def part1(self, puzzle_input: InputType) -> int:
        """Return steps from start to end."""
        start, end, board = puzzle_input
        return self.get_steps([start], end, board)

    def part2(self, puzzle_input: InputType) -> int:
        """Return steps from any low point to end."""
        _, end, board = puzzle_input
        starts = [
            point
            for point, height in board.items()
            if height == 0
        ]
        return self.get_steps(starts, end, board)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        parser = aoc.CoordinatesParserC()
        data = parser.parse(puzzle_input)
        start = data["S"].pop()
        end = data["E"].pop()
        heights = {b: a for a, b in enumerate(string.ascii_lowercase)}
        heights["S"] = heights["a"]
        heights["E"] = heights["z"]
        height_map = {p: heights[c] for p, c in data.chars.items()}

        return start, end, height_map
