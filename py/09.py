#!/bin/python

import collections
import itertools
import util
import re
import sys
import time
from typing import List, Dict


SAMPLE = """\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""


TESTS = (
  util.TestCase(inputs=SAMPLE, part=1, want=127),
  util.TestCase(inputs=SAMPLE, part=2, want=62),
)


def is_valid(pool: List[int], num: int):
  """Return if `num` is the sum of two values from the pool."""
  for a, b in itertools.combinations(pool, 2):
    if a + b == num:
      return True
  return False


def part1(nums: List[int], preamble: int) -> int:
  """Return the first number not composed of two values in the last `preamble` values."""
  pool = nums[0:preamble]
  nums = nums[preamble:]
  for num in nums:
    if not is_valid(pool, num):
      return num
    pool.pop(0)
    pool.append(num)
  raise ValueError


def part2(nums: List[int], preamble: int) -> int:
  """Find a contiguous set of nums that sum to `part1()`. Return min(pool) + max(pool)."""
  want = part1(nums, preamble)
  for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
      s = sum(nums[i:j])
      if s == want:
        return min(nums[i:j]) + max(nums[i:j])
      if s > want:
        break
  raise ValueError


CONFIG = {
  'debug': False,
  'funcs': {1: part1, 2: part2},
  'tranform': int,
  'tests': TESTS,
  'sep': '\n',
  'test_args': [5],
  'run_args': [25],
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
    print(func(data, 25))


if __name__ == '__main__':
  main()

# vim:ts=2:sw=2:expandtab
