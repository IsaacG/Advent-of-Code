#!/usr/bin/env python
"""Day 15. Van Eck sequence. https://www.youtube.com/watch?v=etMJxB-igrc - Numberphile."""

from typing import List

from lib import aoc


class Day15(aoc.Challenge):
  """Solve for the n'th value in a Van Eck sequence."""

  INPUT_PARSER = aoc.ParseOneWord(lambda s: [int(i) for i in s.split(',')])

  TESTS = [
    aoc.TestCase(inputs='0,3,6', part=1, want=436),
    aoc.TestCase(inputs='1,3,2', part=1, want=1),
    aoc.TestCase(inputs='2,1,3', part=1, want=10),
  ]

  def part1(self, puzzle_input: List[List[int]]) -> int:
    return self.solve(puzzle_input, 2020)

  def part2(self, puzzle_input: List[List[int]]) -> int:
    return self.solve(puzzle_input, 30000000)

  def solve(self, starting: List[int], end: int) -> int:
    """Solve Van Eck's n'th digit.

    1st pass: store the last two timestamps. 30s.
    2nd pass: store the last timestamp in a map. 15s.
    3rd pass: store the last timestamp in a list. 8.5s.
    """
    time_said = [0] * end
    for i, j in enumerate(starting[:-1]):
      time_said[j] = i + 1
    last_spoken = starting[-1]

    for counter in range(len(starting), end):
      if not time_said[last_spoken]:
        say = 0
      else:
        say = counter - time_said[last_spoken]
      time_said[last_spoken] = counter
      last_spoken = say
    return last_spoken
