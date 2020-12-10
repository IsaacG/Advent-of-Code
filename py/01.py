#!/bin/python

import sys
import util
from typing import List, Set


def prod_of_pair(pair_sum: int, data: Set[int]) -> int:
  vals = [i for i in data if (pair_sum - i) in data]
  if not vals:
    return 0
  if len(vals) == 2:
    return vals[0] * vals[1]
  raise ValueError(f'Found too many matches.')


def part1(data: List[str]) -> int:
  return prod_of_pair(2020, data)


def part2(data: List[str]) -> int:
  for n in data:
    subset = list(data)
    subset.remove(n)
    prod = prod_of_pair(2020 - n, subset)
    if prod:
      prod *= n
      return prod


CONFIG = {
  'debug': False,
  'funcs': {1: part1, 2: part2},
  'tranform': int,
  'tests': (),
  'sep': '\n',
}


if __name__ == '__main__':
  util.run_day(CONFIG)

# vim:ts=2:sw=2:expandtab
