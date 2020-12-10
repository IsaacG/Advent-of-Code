#!/bin/python

import sys
import util

from typing import List, Dict

SAMPLE = [
  'abc\n\na\nb\nc\n\nab\nac\n\na\na\na\na\n\nb',
  "abc\n\na\nb\nc\n\nab\nac\n\na\na\na\na\n\nb",
]

TESTS = (
  util.TestCase(inputs=SAMPLE[0], part=1, want=11),
  util.TestCase(inputs=SAMPLE[1], part=2, want=6),
)

def part1(data: List[str]) -> int:
  """Part 1: count the unique chars, joining all lines."""
  return sum(len(set(l.replace('\n', ''))) for l in data)


def part2(data: List[str]) -> int:
  """Part 2: count num of chars found on all lines."""
  total = 0
  for r in data:
    records = r.split()
    s = set(records.pop())
    while records:
      s &= set(records.pop())
    total += len(s)
  return total


CONFIG = {
  'debug': False,
  'funcs': {1: part1, 2: part2},
  'tranform': str,
  'tests': TESTS,
  'sep': '\n\n',
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
