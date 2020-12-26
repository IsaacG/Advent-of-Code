#!/bin/pypy3

from typing import List

import typer
from lib import aoc


SAMPLE = """\
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
"""


class Day03(aoc.Challenge):

  TESTS = (
    aoc.TestCase(inputs=SAMPLE, part=1, want=7),
    aoc.TestCase(inputs=SAMPLE, part=2, want=336),
  )

  def tree_count(self, grid, x_step, y_step) -> int:
    count = 0
    x = 0
    for y in range(0, len(grid), y_step):
      if grid[y][x % len(grid[0])] == '#':
        count += 1
      x += x_step
    return count

  def part1(self, grid: List[str]) -> int:
    return self.tree_count(grid, 3, 1)

  def part2(self, grid: List[str]) -> int:
    prod = 1
    for x_step, y_step in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
      prod *= self.tree_count(grid, x_step, y_step)
    return prod


if __name__ == '__main__':
  typer.run(Day03().run)

# vim:ts=2:sw=2:expandtab
