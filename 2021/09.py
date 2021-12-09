#!/bin/python
"""Advent of Code: Day 09."""

import collections
import functools
import math
import re
from typing import Any, Callable

import typer

from lib import aoc

InputType = list[int]

SAMPLE = ["""\
2199943210
3987894921
9856789892
8767896789
9899965678
"""]

class Day09(aoc.Challenge):

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=15),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=1134),
    )

    # Convert lines to type:
    INPUT_TYPES = int
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, lines: InputType) -> int:
        sumt = 0
        for x in range(len(lines[0])):
          for y in range(len(lines)):
            neighs = self.ns(lines, y, x)
            if all(lines[y][x] < neigh for neigh in neighs):
              sumt += lines[y][x] + 1
        return sumt

    def ns(self, lines, y, x):
      neighs = []
      if y > 0:
        neighs.append(lines[y-1][x])
      if x > 0:
        neighs.append(lines[y][x-1])
      if y + 1 < len(lines):
        neighs.append(lines[y+1][x])
      if x + 1 < len(lines[0]):
        neighs.append(lines[y][x+1])
      return neighs

    def n2(self, lines, y, x):
      neighs = []
      if y > 0:
        neighs.append((y-1,x))
      if x > 0:
        neighs.append((y, x-1))
      if y + 1 < len(lines):
        neighs.append((y+1, x))
      if x + 1 < len(lines[0]):
        neighs.append((y, x+1))
      return neighs

    def part2(self, lines: InputType) -> int:
        low = []
        for x in range(len(lines[0])):
          for y in range(len(lines)):
            neighs = self.ns(lines, y, x)
            if all(lines[y][x] < neigh for neigh in neighs):
              low.append((y, x))
        bs = []
        for y, x in low:
          seen = set()
          todo = set([(lines[y][x],y,x)])
          size = 0
          while todo:
            l, a, b = sorted(todo)[0]
            todo.remove((l, a, b))
            if lines[a][b] == 9: continue
            seen.add((a,b))
            ns = [(c,d) for c,d in self.n2(lines, a, b) if (c,d) not in seen]
            if all(lines[c][d] >= lines[a][b] for c,d in ns):
              size += 1
              todo.update((lines[c][d], c,d) for c, d in ns)
          bs.append(size)

        a, b, c = list(sorted(bs, reverse=True))[:3]
        return a * b * c


    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [[int(e) for e in line] for line in puzzle_input.splitlines()]

        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]

        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]


if __name__ == "__main__":
    typer.run(Day09().run)
