#!/bin/pypy3
"""Math parser.

Initial messy code: 0.177/6.108/4.791 ms
I could reverse the tokens to make life easier but that feels like cheating.
"""

import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List, Union


class Node:
  """A node can either be a single number or two nodes with an operator."""
  
  def __init__(self, a, op=None, b=None):
    self.a = a
    self.op = op
    self.b = b
    assert (op is None) == (b is None)
    if op is None:
      assert a.isnumeric()
      assert b is None
    else:
      assert isinstance(a, type(self))
      assert isinstance(b, type(self))

  def compute(self) -> int:
    if self.op is None:
      return int(self.a)
    elif self.op == '*':
      return self.a.compute() * self.b.compute()
    elif self.op == '+':
      return self.a.compute() + self.b.compute()

  def __str__(self):
    if self.op is None:
      return f'({self.a})'
    else:
      return f'({self.a} {self.op} {self.b})'


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

  def preparse_input(self, x):
    """Drop whitespace."""
    return [l.replace(" ", "") for l in x]

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




  def one(self, line):
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
        return self.one(right)
      else:
        if line[i] == '+':
          return self.one(left) + self.one(right)
        if line[i] == '*':
          return self.one(left) * self.one(right)
    else:
      if line.isnumeric():
        return int(line)
      else:
        m = re.search('^(.*)([+*])([0-9]*)$', line)
        assert m
        left, op, right = m.groups()
        left, right = self.one(left), self.one(right)
        if op == "+":
          res = left + right
        if op == '*':
          res = left * right
        return res



    
  def part1(self, lines: List[str]) -> int:
    return sum(self.make_tree(self.tokenize(line)).compute() for line in lines)

  def part2(self, lines: List[str]) -> int:
    return sum(self.two(line) for line in lines)

  def testing(self):
    line = '12+34*(45+34)'
    print(f"Input: {line}")
    tokens = self.tokenize(line)

  def make_tree(self, tokens: List[str]):
    """Build a tree, weird ordering"""
    if len(tokens) == 1:
      return Node(tokens[0])

    # Find the right-most operator and split on that. Treat parens as a block.
    i = len(tokens) - 1
    depth = 0
    while i >= 0:
      if depth == 0 and tokens[i] in '+*':
        left = self.make_tree(tokens[:i])
        op = tokens[i]
        right = self.make_tree(tokens[i+1:])
        return Node(left, op, right)
      if tokens[i] == ')':
        depth += 1
      elif tokens[i] == '(':
        depth -= 1
      i -= 1
    else:
      # Ran out of tokens. Must be "(exp)".
      assert tokens[0] == '(' and tokens[-1] == ')'
      return self.make_tree(tokens[1:-1])


  def tokenize(self, line: str) -> List[str]:
    tokens = []
    i = 0
    ll = len(line)
    while i < ll:
      ss = line[i]
      if ss in '()+*':
        tokens.append(ss)
        i += 1
      else:
        j = i + 1
        while j < ll and line[j] not in '()+*':
          j += 1
        tokens.append(line[i:j])
        i = j
    return tokens


if __name__ == '__main__':
  Day18().run()
  # Day18().testing()

# vim:ts=2:sw=2:expandtab
