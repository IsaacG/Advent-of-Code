#!/bin/python
"""Advent of Code, Day 3: Squares With Three Sides. Count valid triangles."""

from lib import aoc

InputType = list[list[int]]


class Day03(aoc.Challenge):
    """Day 3: Squares With Three Sides."""


    def solver(self, parsed_input: list[list[int]], rotate: bool) -> int:
        """Return the number of valid triangles."""
        if rotate:
            parsed_input = [
                row[i:i + 3]
                for row in zip(*parsed_input)
                for i in range(0, len(row), 3)
            ]
        return sum(2 * max(vals) < sum(vals) for vals in parsed_input)
