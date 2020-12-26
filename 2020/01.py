#!/usr/bin/env pypy

from typing import List, Set
import typer

from lib import aoc

SAMPLE = """\
1721
979
366
299
675
1456
"""


class Day01(aoc.Challenge):

  TESTS = (
    aoc.TestCase(inputs=SAMPLE, part=1, want=514579),
    aoc.TestCase(inputs=SAMPLE, part=2, want=241861950),
  )
  TRANSFORM = int

  def prod_of_pair(self, pair_sum: int, data: Set[int]) -> int:
    vals = [i for i in data if (pair_sum - i) in data]
    if not vals:
      return 0
    if len(vals) == 2:
      return vals[0] * vals[1]
    raise ValueError('Found too many matches.')

  def part1(self, data: List[str]) -> int:
    return self.prod_of_pair(2020, data)

  def part2(self, data: List[str]) -> int:
    for n in data:
      subset = list(data)
      subset.remove(n)
      prod = self.prod_of_pair(2020 - n, subset)
      if prod:
        prod *= n
        return prod


if __name__ == '__main__':
  typer.run(Day01().run)

# vim:ts=2:sw=2:expandtab
