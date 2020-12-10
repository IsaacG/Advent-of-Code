#!/bin/python

import sys
import util

from typing import List


# Translate F to 0, B to 1, L to 0 and R to 1.
transmap = str.maketrans('FBLR', '0101')


def translate(s: str) -> int:
  """Translate to binary string then to int."""
  return int(s.translate(transmap), 2)


TESTS = (
  util.TestCase(inputs='BFFFBBFRRR', part=1, want=567),
  util.TestCase(inputs='FFFBBBFRRR', part=1, want=119),
  util.TestCase(inputs='BBFFBBFRLL', part=1, want=820),
)


def part1(lines: List[str]) -> int:
  # Part one: max seat number
  seats = {translate(r) for r in lines}
  return max(seats)

def part2(lines: List[str]) -> int:
  # Part two: find a gap of one between two seats.
  seats = {translate(r) for r in lines}

  for s in seats:
    if (s + 1) not in seats and (s + 2) in seats:
      return s + 1


CONFIG = {
  'debug': False,
  'funcs': {1: part1, 2: part2},
  'tranform': str,
  'tests': TESTS,
  'sep': '\n',
}


if __name__ == '__main__':
  util.run_day(CONFIG)

# vim:ts=2:sw=2:expandtab
