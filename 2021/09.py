#!/bin/python
"""Advent of Code: Day 09."""

import collections
import dataclasses
import functools
import math
import re
from typing import Any, Callable

import typer

from lib import aoc

InputType = list[list[int]]

SAMPLE = ["""\
2199943210
3987894921
9856789892
8767896789
9899965678
"""]

class Day09(aoc.Challenge):
    """Find low points and basins in a topographic map."""

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=15),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=1134),
    )

    def part1(self, lines: InputType) -> int:
        """Find all the low points on the map."""
        neighbors = (1, -1, -1j, +1j)
        depths = lines
        result = 0
        for xy, depth in depths.items():
          if all(depth < depths[xy + n] for n in neighbors if xy + n in depths):
            result += depth + 1
        return result

    def part2(self, lines: InputType) -> int:
        neighbors = (1, -1, -1j, +1j)
        depths = lines
        low = []
        for xy, depth in depths.items():
          if all(depth < depths[xy + n] for n in neighbors if xy + n in depths):
            low.append(xy)

        basins = []
        for lowpoint in low:
          seen = set()
          todo = set([(depths[lowpoint], lowpoint)])
          size = 0
          while todo:
            depth, xy = sorted(todo, key=lambda x: x[0])[0]
            todo.remove((depth, xy))
            if depth == 9:
              continue
            seen.add(xy)
            ns = [xy + n for n in neighbors if xy+n in depths and xy + n not in seen]
            if all(depths[n] >= depth for n in ns):
              size += 1
              todo.update((depths[n], n) for n in ns)
          basins.append(size)

        a, b, c = list(sorted(basins, reverse=True))[:3]
        return a * b * c


    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        grid = [[int(e) for e in line] for line in puzzle_input.splitlines()]
        depths = {x + y * 1j: grid[x][y] for x in range(len(grid)) for y in range(len(grid[0]))}
        return depths


if __name__ == "__main__":
    typer.run(Day09().run)
