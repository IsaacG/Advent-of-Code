#!/bin/python

import collections
import functools
import math
import re
import sys
import time
import util
from typing import List, Dict, Callable, Any


SAMPLE = ["""\
16
10
15
5
1
11
7
19
6
12
4
""", """\
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
"""
]

TESTS = (
  util.TestCase(inputs=SAMPLE[0], part=1, want=35),
  util.TestCase(inputs=SAMPLE[1], part=1, want=220),
  util.TestCase(inputs=SAMPLE[1], part=2, want=19208),
)


def part1(lines: List[str]) -> int:
  nums = sorted([0] + lines)
  diffs = [nums[i+1] - nums[i] for i in range(len(nums) - 1)] + [3]
  c = collections.Counter(diffs)
  return c[1] * c[3]


def part2(lines: List[str]) -> int:
  nums = sorted([0] + lines + [max(lines) + 3])

  @functools.cache
  def get(i):
    if i >= len(nums):
      return 0
    if i == len(nums) - 1:
      return 1
    valid = []
    for j in (1, 2, 3):
      k = i + j
      try:
        if nums[k] - nums[i] <= 3:
          valid.append(k)
      except IndexError:
        pass
    return sum(get(v) for v in valid)

  return get(0)


CONFIG = {
  'debug': False,
  'funcs': {1: part1, 2: part2},
  'tranform': int,
  'tests': TESTS,
  'sep': '\n',
}


if __name__ == '__main__':
  util.run_day(CONFIG)

# vim:ts=2:sw=2:expandtab
