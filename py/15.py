#!/bin/python

import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List

SAMPLE = ["""\
0,3,6
""", """\
"""]


class Day15(aoc.Challenge):

  TRANSFORM = lambda _, s: [int(i) for i in s.split(',')]
  DEBUG = True

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=436),
    aoc.TestCase(inputs=SAMPLE[0], part=2, want=175594),
  )

  def part1(self, lines: List[str]) -> int:
    starting = lines[0]
    ages = collections.defaultdict(list)
    counter = 1
    last = None
    is_new = False
    for s in starting:
      last = s
      is_new = last not in ages
      ages[s].insert(0, counter)
      counter += 1

    while True:
      if is_new:
        s = 0
      else:
        s = ages[last][0] - ages[last][1]
      last = s
      is_new = last not in ages
      ages[s].insert(0, counter)
      ages[s] = ages[s][0:2]
      if counter == 2020: return last
      counter += 1
        
  def part2(self, lines: List[str]) -> int:
    starting = lines[0]
    ages = collections.defaultdict(list)
    counter = 1
    last = None
    is_new = False
    for s in starting:
      last = s
      is_new = last not in ages
      ages[s].insert(0, counter)
      counter += 1

    while True:
      if is_new:
        s = 0
      else:
        s = ages[last][0] - ages[last][1]
      last = s
      is_new = last not in ages
      ages[s].insert(0, counter)
      ages[s] = ages[s][0:2]
      if counter == 30000000: return last
      counter += 1
        




if __name__ == '__main__':
  Day15().run()

# vim:ts=2:sw=2:expandtab
SAMPLE = ["""\

"""]
# vim:ts=2:sw=2:expandtab
