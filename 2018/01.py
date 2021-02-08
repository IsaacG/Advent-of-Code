#!/bin/python
"""Day 1: Chronal Calibration.

Sum up frequencies then do so repeatedly until a repeat is seen.
"""

import itertools
import typer
from typing import List

from lib import aoc


class Day01(aoc.Challenge):

  def part1(self, lines: List[int]) -> int:
    return sum(lines)

  def part2(self, lines: List[int]) -> int:
    seen = set()
    freq = 0
    it = itertools.cycle(lines)
    while freq not in seen:
      seen.add(freq)
      freq += next(it)
    return freq

  def parse_input(self, puzzle_input: str) -> List[int]:
    return [int(i) for i in puzzle_input.split('\n')]


if __name__ == '__main__':
  typer.run(Day01().run)

# vim:ts=2:sw=2:expandtab
