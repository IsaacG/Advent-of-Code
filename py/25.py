#!/bin/pypy3
"""Brute force solve Diffie Hellman key exchange."""

import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List


class Day25(aoc.Challenge):
  """Day 25. Brute force solve Diffie Hellman key exchange."""

  TRANSFORM = int

  TESTS = (
    aoc.TestCase(inputs="5764801\n17807724\n", part=1, want=14897079),
  )

  def transform(self, subject: int, loop_counter: int) -> int:
    """Apply the transform function."""
    num = 1
    for i in range(loop_counter):
      num = (num * subject) % 20201227
    return num
    
  def force(self, result, subject):
    """Brute force the loop_counter to "solve" Diffie Hellman."""
    attempt = 0
    num = 1
    while num != result:
      attempt += 1
      num = (num * subject) % 20201227
    return attempt

  def part1(self, lines: List[str]) -> int:
    b = self.force(lines[1], 7)
    # a = self.force(lines[0], 7)
    # print(1, a)
    return self.transform(lines[0], b)
  
  def part2(self, lines: List[str]) -> int:
    return 0


if __name__ == '__main__':
  Day25().run()

# vim:ts=2:sw=2:expandtab
