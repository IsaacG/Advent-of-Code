#!/bin/python
"""Advent of Code, Day 12: Hill Climbing Algorithm. Solve for the shortest path through a maze."""

import string
import collections

from lib import aoc


def get_steps(starts: list[complex], end: complex, board: dict[complex, int]) -> int:
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


def solve(data: tuple[complex, complex, dict[complex, int]], part: int) -> int:
    """Return steps to the end."""
    start, end, board = data
    if part == 1:
        return get_steps([start], end, board)

    starts = [
        point
        for point, height in board.items()
        if height == 0
    ]
    return get_steps(starts, end, board)


def input_parser(puzzle_input: str) -> tuple[complex, complex, dict[complex, int]]:
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


SAMPLE = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
TESTS = [(1, SAMPLE, 31), (2, SAMPLE, 29)]
