#!/bin/pypy3

import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List

SAMPLE = ["""\
""", """\
"""]


class Day18(aoc.Challenge):

  TRANSFORM = str

  TESTS = (
    aoc.TestCase(part=1, inputs="2 * 3 + (4 * 5)", want=26),
    aoc.TestCase(part=1, inputs="5 + (8 * 3 + 9 + 3 * 4 * 3)", want=437),
    aoc.TestCase(part=1, inputs="5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", want=12240),
    aoc.TestCase(part=1, inputs="((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", want=13632),
    aoc.TestCase(part=2, inputs="1 + (2 * 3) + (4 * (5 + 6))", want=51),
    aoc.TestCase(part=2, inputs="2 * 3 + (4 * 5)", want=46),
    aoc.TestCase(part=2, inputs="5 + (8 * 3 + 9 + 3 * 4 * 3)", want=1445),
    aoc.TestCase(part=2, inputs="5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", want=669060),
    aoc.TestCase(part=2, inputs="((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", want=23340),
  )

  def two(self, line):
    if re.match(r'^[0-9]+$', line):
      return int(line)

    if '(' in line:
      start = 0
      while line[start] != '(':
        start += 1
      i = start
      count = 1
      while count:
        i += 1
        if line[i] == ')':
          count -= 1
        if line[i] == '(':
          count += 1
      left, p, right = line[:start], line[start+1:i], line[i+1:]
      line = left + str(self.two(p)) + right
      return self.two(line)
    
    if '*' in line:
      i = len(line) - 1
      while line[i] != '*':
        i -= 1
      return self.two(line[:i]) * self.two(line[i+1:])
    if '+' in line:
      i = len(line) - 1
      while line[i] != '+':
        i -= 1
      return self.two(line[:i]) + self.two(line[i+1:])




  def prse(self, line):
    if line.isnumeric():
      return int(line)

    i = len(line) - 1
    if line[i] == ")":
      count = 1
      i -= 1
      while count:
        if line[i] == "(":
          count -= 1
        if line[i] == ")":
          count += 1
        i -= 1
      if i == -1:
        left, right = "", line[1:-1]
      else:
        left, right = line[0:i], line[i+2:-1]
      if not left:
        return self.prse(right)
      else:
        if line[i] == '+':
          return self.prse(left) + self.prse(right)
        if line[i] == '*':
          return self.prse(left) * self.prse(right)
    else:
      if line.isnumeric():
        return int(line)
      else:
        m = re.search('^(.*)([+*])([0-9]*)$', line)
        assert m
        left, op, right = m.groups()
        left, right = self.prse(left), self.prse(right)
        if op == "+":
          res = left + right
        if op == '*':
          res = left * right
        return res



    
  def part1(self, lines: List[str]) -> int:
    return sum(self.prse(line.replace(" ", "")) for line in lines)

  def part2(self, lines: List[str]) -> int:
    return sum(self.two(line.replace(" ", "")) for line in lines)


if __name__ == '__main__':
  Day18().run()

# vim:ts=2:sw=2:expandtab
