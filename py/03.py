#!/bin/python

import sys
import util

from typing import List


def tree_count(grid, x_step, y_step) -> int:
  count = 0
  x = 0
  for y in range(0, len(grid), y_step):
    if grid[y][x % len(grid[0])] == '#':
      count += 1
    x += x_step
  return count


def part1(grid: List[str]) -> int:
  return tree_count(grid, 3, 1)


def part2(grid: List[str]) -> int:
  prod = 1
  for x_step, y_step in ((1,1), (3,1), (5,1), (7,1), (1,2)):
    prod *= tree_count(grid, x_step, y_step)
  return prod


CONFIG = {
  'debug': False,
  'funcs': {1: part1, 2: part2},
  'tranform': str,
  'tests': (),
  'sep': '\n',
}


if __name__ == '__main__':
  util.run_day(CONFIG)

# vim:ts=2:sw=2:expandtab
