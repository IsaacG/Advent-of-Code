#!/bin/python

import collections
import functools
import math
import re
import typer
from typing import Any, Callable, Dict, List

from lib import aoc


SAMPLE = ["""\
199
200
208
210
200
207
240
269
260
263
"""]


class Day01(aoc.Challenge):

  DEBUG = True

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=7),
    aoc.TestCase(inputs=SAMPLE[0], part=2, want=5),
  )

  def part1(self, lines: List[int]) -> int:
    return sum(b > a for a, b in zip(lines, lines[1:]))

  def part2(self, lines: List[int]) -> int:
    groups = [a + b + c for a, b, c in zip(lines, lines[1:], lines[2:])]
    return sum(b > a for a, b in zip(groups, groups[1:]))

  def parse_input(self, puzzle_input: str):
    return [int(i) for i in puzzle_input.split('\n')]
    return puzzle_input.split('\n')
    return puzzle_input


if __name__ == '__main__':
  typer.run(Day01().run)

# vim:ts=2:sw=2:expandtab
