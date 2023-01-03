#!/usr/bin/env python
"""2019 Day 01: The Tyranny of the Rocket Equation."""

import typer
from typing import List

from lib import aoc


class Day01(aoc.Challenge):
  """Compute fuel costs."""

  TESTS = (
    aoc.TestCase(inputs="12", part=1, want=2),
    aoc.TestCase(inputs="14", part=1, want=2),
    aoc.TestCase(inputs="1969", part=1, want=654),
    aoc.TestCase(inputs="100756", part=1, want=33583),

    aoc.TestCase(inputs="14", part=2, want=2),
    aoc.TestCase(inputs="1969", part=2, want=966),
    aoc.TestCase(inputs="100756", part=2, want=50346),
  )
  INPUT_PARSER = aoc.parse_one_int_per_line

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

  def part2(self, parsed_input: List[int]) -> int:
    return self.sum_map(parsed_input, self.fuel)

  def part1(self, parsed_input: List[int]) -> int:
    return self.sum_map(parsed_input, self.simple_fuel)


if __name__ == '__main__':
  typer.run(Day01().run)

# vim:ts=2:sw=2:expandtab
