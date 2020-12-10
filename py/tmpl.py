#!/bin/python

import collections
import functools
import math
import re
import sys
import time
import util
from typing import List, Dict

SAMPLE = ["""\
1
""", """\
"""]


TESTS = (
  util.TestCase(inputs=SAMPLE[0], part=1, want=0),
)

def part1(lines: List[str]) -> int:
  return 0


def part2(lines: List[str]) -> int:
  return 0


CONFIG = {
  'tranform': str,
  'debug': True,
  'funcs': {1: part1, 2: part2},
  'tests': TESTS,
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
