#!/bin/pypy3

import pathlib
import re
import sys
from typing import List, Tuple

import aoc

RE = re.compile('^([0-9]+)-([0-9]+) (.): (.*)$')

SAMPLE = """\
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
"""

class Day02(aoc.Challenge):

  TESTS = (
    aoc.TestCase(inputs=SAMPLE, part=1, want=2),
    aoc.TestCase(inputs=SAMPLE, part=2, want=1),
  )

  def preparse_input(self, lines: List[str]) -> Tuple[int, int, str, str]:
    data = []
    for line in lines:
      r = RE.match(line)
      mn, mx, char, passwd = r.groups()
      data.append((int(mn), int(mx), char, passwd))
    return data

  def part1(self, data) -> int:
    return len([
      True for (mn, mx, char, passwd) in data
      if mn <= len([1 for i in passwd if i == char]) <= mx
    ])

  def part2(self, data) -> int:
    return len([
      True for (mn, mx, char, passwd) in data
      if (passwd[mn - 1] == char) ^ (passwd[mx - 1] == char)
    ])


if __name__ == '__main__':
  Day02().run()

# vim:ts=2:sw=2:expandtab
