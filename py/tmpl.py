#!/bin/python

import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List

SAMPLE = ["""\
1
""", """\
"""]


class DayNN(aoc.Challenge):

  TRANSFORM = int
  DEBUG = True

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=0),
  )

  def part1(self, lines: List[str]) -> int:
    return 0

  def part2(self, lines: List[str]) -> int:
    return 0


if __name__ == '__main__':
  DayNN().run()

# vim:ts=2:sw=2:expandtab
