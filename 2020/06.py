#!/usr/bin/env pypy

import typer
from lib import aoc
from typing import List

SAMPLE = [
  'abc\n\na\nb\nc\n\nab\nac\n\na\na\na\na\n\nb',
  "abc\n\na\nb\nc\n\nab\nac\n\na\na\na\na\n\nb",
]


class Day06(aoc.Challenge):

  SEP = '\n\n'
  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=11),
    aoc.TestCase(inputs=SAMPLE[1], part=2, want=6),
  )

  def part1(self, data: List[str]) -> int:
    """Part 1: count the unique chars, joining all lines."""
    return aoc.sum_map(data, lambda l: len(set(l.replace('\n', ''))))

  def part2(self, data: List[str]) -> int:
    """Part 2: count num of chars found on all lines."""
    total = 0
    for r in data:
      records = r.split()
      s = set(records.pop())
      while records:
        s &= set(records.pop())
      total += len(s)
    return total


if __name__ == '__main__':
  typer.run(Day06().run)

# vim:ts=2:sw=2:expandtab
