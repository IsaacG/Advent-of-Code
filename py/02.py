#!/bin/python

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

  def parse(self, line: str) -> Tuple[int, int, str, str]:
     r = RE.match(line)
     mn, mx, char, passwd = r.groups()
     return int(mn), int(mx), char, passwd

  def valid_a(self, line: str) -> bool:
     mn, mx, char, passwd = self.parse(line)
     match = len([1 for i in passwd if i == char])
     return mn <= match <= mx

  def valid_b(self, line: str) -> bool:
     mn, mx, char, passwd = self.parse(line)
     return (passwd[mn - 1] == char) ^ (passwd[mx - 1] == char)
     return mn <= match <= mx

  def part1(self, lines: List[str]) -> int:
    return len([1 for line in lines if self.valid_a(line)])

  def part2(self, lines: List[str]) -> int:
    return len([1 for line in lines if self.valid_b(line)])


if __name__ == '__main__':
  Day02().run()

# vim:ts=2:sw=2:expandtab
