#!/bin/python
"""Day 15. Van Eck sequence. https://www.youtube.com/watch?v=etMJxB-igrc - Numberphile."""

import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List


class Day15(aoc.Challenge):
  """Solve for the n'th value in a Van Eck sequence."""

  TRANSFORM = lambda _, s: [int(i) for i in s.split(',')]
  SLOW = True, True

  TESTS = (
    aoc.TestCase(inputs='0,3,6', part=1, want=436),
    aoc.TestCase(inputs='1,3,2', part=1, want=1),
    aoc.TestCase(inputs='2,1,3', part=1, want=10),
  )

  def part1(self, lines: List[List[int]]) -> int:
    return self.solve(lines[0], 2020)
        
  def part2(self, lines: List[List[int]]) -> int:
    return self.solve(lines[0], 30000000)

  def solve(self, starting: List[int], end: int) -> int:
    time_said = {j: i for i, j in enumerate(starting[:-1])}
    last_spoken = starting[-1]

    for counter in range(len(starting), end):
      if last_spoken not in time_said:
        say = 0
      else:
        say = counter - 1 - time_said[last_spoken]
      time_said[last_spoken] = counter - 1
      last_spoken = say
    return last_spoken


if __name__ == '__main__':
  Day15().run()

# vim:ts=2:sw=2:expandtab
