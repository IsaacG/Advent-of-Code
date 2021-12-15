#!/bin/python

import collections
import functools
import math
import re
import typer
from typing import Any, Callable, Dict, List

from lib import aoc


class DayNN(aoc.Challenge):

  DEBUG = True

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=0),
  )

  def part1(self, parsed_input: List[str]) -> int:
    return 0

  def parse_input(self, puzzle_input: str):
    return puzzle_input.split('\n')
    return puzzle_input
    return [int(i) for i in puzzle_input.split('\n')]


if __name__ == '__main__':
  typer.run(DayNN().run)

# vim:ts=2:sw=2:expandtab
