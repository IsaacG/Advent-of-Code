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


if __name__ == '__main__':
  util.run_day(CONFIG)

# vim:ts=2:sw=2:expandtab
