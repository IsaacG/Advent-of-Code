#!/bin/python
"""Advent of Code, Day 12: Hill Climbing Algorithm."""

import string
import collections
import queue
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = [
    """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""",
]

LineType = int
InputType = list[LineType]


class Day12(aoc.Challenge):
    """Day 12: Hill Climbing Algorithm."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=31),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=29),
    ]

    def part1(self, parsed_input: InputType) -> int:
        start, end, board = parsed_input
        step_count = {start: 0}

        todo = {start}
        visited = set()

        while todo:
            point = min(todo, key=lambda p: step_count[p])
            todo.remove(point)
            visited.add(point)
            for n in board.neighbors(point, False):
                if board[n] - 1 > board[point]:
                    continue
                if n in step_count and step_count[n] <= step_count[point] + 1:
                    continue
                step_count[n] = step_count[point] + 1
                todo.add(n)

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

            todo = {start}
            visited = set()

            while todo:
                point = min(todo, key=lambda p: step_count[p])
                todo.remove(point)
                visited.add(point)
                for n in board.neighbors(point, False):
                    if board[n] - 1 > board[point]:
                        continue
                    if n in step_count and step_count[n] <= step_count[point] + 1:
                        continue
                    step_count[n] = step_count[point] + 1
                    todo.add(n)

            if end in step_count:
                options.append(step_count[end])
        return min(options)

    def part1_a(self, parsed_input: InputType) -> int:
        start, end, board = parsed_input
        options = collections.defaultdict(list)
        for p, height in board.items():
            for direction in aoc.DIRECTIONS:
                if p + direction not in board:
                    continue
                if board[p] +1 < board[p + direction]:
                    continue
                improvement = board[p] - board[p + direction]
                options[p].append((improvement, p + direction))

        todo = queue.PriorityQueue()
        for improvement, neighbor in options[start]:
            todo.put((1, improvement, neighbor.real, neighbor.imag))

        visited = {start}
        while not todo.empty():
            steps, cost, px, py = todo.get()
            point = complex(px, py)
            visited.add(point)
            for improvement, neighbor in options[point]:
                if neighbor == end:
                    return steps + 1
                if neighbor in visited:
                    continue
                todo.put((steps + 1, cost + improvement, neighbor.real, neighbor.imag))

        raise RuntimeError


    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        heights = {}
        start = None
        end = None
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
