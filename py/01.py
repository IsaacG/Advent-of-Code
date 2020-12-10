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


# ######################################### #
# Fixed code. Probably do not need to edit. #

debug = lambda x: util.debug(CONFIG, x)

def main():
  """Run the tests then the problems."""
  util.run_tests(CONFIG)

  data = util.load_data(sys.argv[1], config=CONFIG)
  for i, func in enumerate((part1, part2)):
    debug(f"Running part {i + 1}:")
    print(func(data))


if __name__ == '__main__':
  main()

# vim:ts=2:sw=2:expandtab
