#!/usr/bin/env python
"Day 10. Power adapters."""

import collections
import functools
from typing import List

import typer
from lib import aoc


SAMPLE = [
  """\
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


class Day10(aoc.Challenge):
  """Solution to Day 10."""

  INPUT_TYPES = int

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=35),
    aoc.TestCase(inputs=SAMPLE[1], part=1, want=220),
    aoc.TestCase(inputs=SAMPLE[1], part=2, want=19208),
  )

  def part1(self, parsed_input: List[int]) -> int:
    """Count the 1-steps and 3-steps."""
    # Sort the plugs.
    nums = sorted(parsed_input)
    # Add the source and dest, 0 and max+3.
    nums.insert(0, 0)
    nums.append(max(nums) + 3)
    # Compute the size of each step.
    diffs = [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]
    # Count and multiply.
    counts = collections.Counter(diffs)
    return counts[1] * counts[3]

  def part2(self, parsed_input: List[int]) -> int:
    """Count all possible paths from 0 to dest."""
    nums = [0] + sorted(parsed_input) + [max(parsed_input) + 3]

    @functools.cache
    def possible_paths_from(i):
      """Compute all possible paths from node i to the end.

      Paths from N-1 to N = 1.
      Paths from M to N = sum(
          all paths from v to N
          for all valid next-nodes v
      ).
      Valid next-nodes are any nodes within 3 of M.

      Dynamic programming ahead. Cache result.
      """
      if i == len(nums) - 1:
        return 1
      valid = [
        j for j in range(i + 1, min(i + 4, len(nums)))
        if nums[j] - nums[i] <= 3
      ]
      return self.sum_map(valid, possible_paths_from)

    return possible_paths_from(0)


if __name__ == '__main__':
  typer.run(Day10().run)

# vim:ts=2:sw=2:expandtab
