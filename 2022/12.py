#!/bin/python
"""Advent of Code, Day 12: Hill Climbing Algorithm."""

import string
import collections

import typer
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

    def part1(self, parsed_input: InputType) -> int:
        start, end, board = parsed_input
        step_count = {start: 0}

        todo = collections.deque([start])
        visited = set()

        while todo:
            point = todo.popleft()
            visited.add(point)
            for n in board.neighbors(point, False):
                if board[n] - 1 > board[point]:
                    continue
                if n in step_count and step_count[n] <= step_count[point] + 1:
                    continue
                step_count[n] = step_count[point] + 1
                todo.append(n)

        if end in step_count:
            return step_count[end]
        raise RuntimeError

    def part2(self, parsed_input: InputType) -> int:
        start, end, board = parsed_input

        options = []
        for start in board:
            if board[start] != 0:
                continue

            step_count = {start: 0}

            todo = collections.deque([start])
            visited = set()

            while todo:
                point = todo.popleft()
                visited.add(point)
                for n in board.neighbors(point, False):
                    if board[n] - 1 > board[point]:
                        continue
                    if n in step_count and step_count[n] <= step_count[point] + 1:
                        continue
                    step_count[n] = step_count[point] + 1
                    todo.append(n)

            if end in step_count:
                options.append(step_count[end])
        return min(options)

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

        return start, end, aoc.Board(heights)


if __name__ == "__main__":
    typer.run(Day12().run)

# vim:expandtab:sw=4:ts=4
