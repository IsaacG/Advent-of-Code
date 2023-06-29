#!/usr/bin/env python
"""2019 Day 4: Secure Container"""

import collections
from typing import Callable, List

from lib import aoc

LEN = 6


class Day04(aoc.Challenge):
  """Day 4. Count valid passwords (incrementing, double num, in range)."""

  TESTS = (
    aoc.TestCase(inputs='100000-111111', part=1, want=1),
    aoc.TestCase(inputs='100000-111115', part=1, want=5),
    aoc.TestCase(inputs='100000-111123', part=2, want=1),
  )

  def has_a_repeat(self, num: int) -> bool:
    """Must contain a doubled digit."""
    digits = [int(i) for i in str(num)]
    return any(digits[i + 1] == digits[i] for i in range(LEN - 1))

  def has_a_double(self, num: int) -> bool:
    """Must contain a doubled - not tripled or more - digit."""
    digits = collections.Counter(str(num))
    return 2 in digits.values()

  def part2(self, bounds: List[int]) -> int:
    """Count valid passwords, using the has_a_double rule."""
    return self.solve(bounds, lambda x: self.has_a_double(x))

  def part1(self, bounds: List[int]) -> int:
    """Count valid passwords, using the has_a_repeat rule."""
    return self.solve(bounds, lambda x: self.has_a_repeat(x))

  def solve(self, bounds: List[int], valid: Callable[[int], bool]) -> int:
    """Count the number of "valid" passwords in a range.

    Build the number one digit at a time, bounds checking each time.
    If the bounds are 200 <= n <= 350,
    then we can check 2 <= 3 <= 3 at len=1 and 20 <= 36 <= 35 at len=2.
    """
    part_bounds = [[0] + [int(str(num)[:i]) for i in range(1, LEN + 1)] for num in bounds]
    self.c = 20

    def sum_valid(num: int, length: int) -> int:
      """Recursively count sum valid passwords for a given prefix."""
      # Check early at each length for bounds.
      if not part_bounds[0][length] <= num <= part_bounds[1][length]:
        if self.c:
          self.c -= 1
        return 0
      if length == LEN:
        return 1 if valid(num) else 0

      # Next digit to add must be >= prior digit.
      prior_digit = num % 10
      num *= 10
      length += 1
      return sum(sum_valid(num + i, length) for i in range(prior_digit, 10))

    # The first digit cannot be 0 or it won't be a "6 digit number".
    # Or at least, it won't be in the range given by my input.
    return sum(sum_valid(num, 1) for num in range(1, 10))

  def input_parser(self, puzzle_input: str):
    return [int(i) for i in puzzle_input.split('-')]
