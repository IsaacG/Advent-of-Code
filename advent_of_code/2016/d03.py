#!/bin/python
"""Advent of Code, Day 3: Squares With Three Sides. Count valid triangles."""

from collections import abc
from lib import aoc

InputType = list[list[int]]


class Day03(aoc.Challenge):
    """Day 3: Squares With Three Sides."""

    def solver(self, puzzle_input: list[abc.Iterable[int]], part_one: bool) -> int:
        """Return the number of valid triangles."""
        if not part_one:
            puzzle_input = [
                row[i:i + 3]
                for row in zip(*puzzle_input)
                for i in range(0, len(row), 3)
            ]
        return sum(2 * max(vals) < sum(vals) for vals in puzzle_input)
