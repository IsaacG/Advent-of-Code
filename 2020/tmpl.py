#!/bin/pypy3

import aoc
import collections
import functools
import math
import re
import typer
from typing import Any, Callable, Dict, List


class DayNN(aoc.Challenge):

  TRANSFORM = str
  DEBUG = True
  SEP = '\n'

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=0),
  )

  def part1(self, lines: List[str]) -> int:
    return 0

  def preparse_input(self, x):
    return x


if __name__ == '__main__':
  typer.run(DayNN().run)

# vim:ts=2:sw=2:expandtab
