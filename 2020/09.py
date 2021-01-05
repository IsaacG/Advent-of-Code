#!/usr/bin/env pypy
"""Day 9."""

import itertools
from typing import List

import typer
from lib import aoc

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


class Day09(aoc.Challenge):
  """Day 9."""

  TRANSFORM = int

  TESTS = (
    aoc.TestCase(inputs=SAMPLE, part=1, want=127),
    aoc.TestCase(inputs=SAMPLE, part=2, want=62),
  )

  def is_valid(self, pool: List[int], num: int):
    """Return if `num` is the sum of two values from the pool."""
    for a, b in itertools.combinations(pool, 2):
      if a + b == num:
        return True
    return False

  def part1(self, nums: List[int]) -> int:
    """Return the first number not composed of two values in the last `preamble` values."""
    preamble = 5 if self.testing else 25
    pool = nums[0:preamble]
    nums = nums[preamble:]
    for num in nums:
      if not self.is_valid(pool, num):
        return num
      pool.pop(0)
      pool.append(num)
    raise ValueError

  def part2(self, nums: List[int]) -> int:
    """Find a contiguous set of nums that sum to `part1()`. Return min(pool) + max(pool)."""
    want = self.part1(nums)
    for i in range(len(nums)):
      for j in range(i + 1, len(nums)):
        s = sum(nums[i:j])
        if s == want:
          return min(nums[i:j]) + max(nums[i:j])
        if s > want:
          break
    raise ValueError


if __name__ == '__main__':
  typer.run(Day09().run)

# vim:ts=2:sw=2:expandtab
