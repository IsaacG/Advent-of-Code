#!/bin/pypy3
"""2019 Day 01.

Day 1: The Tyranny of the Rocket Equation
https://adventofcode.com/2019/day/1
"""

import aoc
import typer
from typing import Any, Callable, Dict, List


class Day01(aoc.Challenge):

  TRANSFORM = int

  TESTS = (
    aoc.TestCase(inputs="12", part=1, want=2),
    aoc.TestCase(inputs="14", part=1, want=2),
    aoc.TestCase(inputs="1969", part=1, want=654),
    aoc.TestCase(inputs="100756", part=1, want=33583),

    aoc.TestCase(inputs="14", part=2, want=2),
    aoc.TestCase(inputs="1969", part=2, want=966),
    aoc.TestCase(inputs="100756", part=2, want=50346),
  )

  def fuel(self, mass):
    """Sum fuel needed for some mass and all its fuel."""
    total = 0
    unfueled = self.simple_fuel(mass)
    while unfueled:
      total += unfueled
      unfueled = self.simple_fuel(unfueled)
    return total

  def simple_fuel(self, mass):
    """Direct fuel needed for some mass."""
    return max(0, int(mass / 3) - 2)

  def part2(self, lines: List[int]) -> int:
    return aoc.sum_map(lines, self.fuel)

  def part1(self, lines: List[int]) -> int:
    return aoc.sum_map(lines, self.simple_fuel)


if __name__ == '__main__':
  typer.run(Day01().run)

# vim:ts=2:sw=2:expandtab
