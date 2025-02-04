#!/usr/bin/env python

from lib import aoc

SAMPLE = [
  'abc\n\na\nb\nc\n\nab\nac\n\na\na\na\na\n\nb',
  "abc\n\na\nb\nc\n\nab\nac\n\na\na\na\na\n\nb",
]


class Day06(aoc.Challenge):

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=11),
    aoc.TestCase(inputs=SAMPLE[1], part=2, want=6),
  )

  def part1(self, data: list[str]) -> int:
    """Part 1: count the unique chars, joining all lines."""
    return sum(len(set(l.replace('\n', ''))) for l in data)

  def part2(self, data: list[str]) -> int:
    """Part 2: count num of chars found on all lines."""
    total = 0
    for r in data:
      records = r.split()
      s = set(records.pop())
      while records:
        s &= set(records.pop())
      total += len(s)
    return total

  def input_parser(self, puzzle_input: str):
    return puzzle_input.split('\n\n')
