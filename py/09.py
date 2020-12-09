#!/bin/python

import collections
import itertools
from util import load_data
import re
import time
from typing import List, Dict


SAMPLE1 = """\
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

TEST_DATA = {
  'input1': SAMPLE1,
  'input2': SAMPLE1,
  'want1': 127,
  'want2': 62,
}


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


# ######################################### #
# Fixed code. Probably do not need to edit. #

def get_func(i):
  if i == 1:
    return part1
  elif i == 2:
    return part2
  else:
    raise ValueError(f'Bad part {i}')


def test():
  """Assert solution works."""
  for i in (1, 2):
    if TEST_DATA[f'input{i}'].strip() and TEST_DATA[f'want{i}']:
      sample_text = TEST_DATA[f'input{i}']
      sample_data = load_data(text=sample_text, func=int)
      func = get_func(i)
      want = TEST_DATA[f'want{i}']
      got = func(sample_data, 5)
      assert want == got, f'part{i}: want({want}) != got({got})'


def main():
  test()
  data = load_data(func=int)
  for i in (1, 2):
    if TEST_DATA[f'input{i}'].strip():
      func = get_func(i)
      print(func(data, 25))


if __name__ == '__main__':
  main()

# vim:ts=2:sw=2:expandtab
