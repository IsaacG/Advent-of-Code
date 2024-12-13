#!/usr/bin/env python
"""Math parser.

Initial messy code: 0.177/6.108/4.791 ms
I could reverse the tokens to make life easier but that feels like cheating.
Part 1, non-parameterized conds test: 3.313 ms
With the tree parser: 0.178/4.177/4.783 ms
"""

from typing import Callable, List, Optional
from lib import aoc


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
    # Moving these for a map kills runtime.
    elif self.op == '*':
      return self.a.compute() * self.b.compute()
    elif self.op == '+':
      return self.a.compute() + self.b.compute()
    else:
      raise RuntimeError

  def __str__(self):
    if self.op is None:
      return self.a
    else:
      return f'({self.a} {self.op} {self.b})'


class Day18(aoc.Challenge):

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

  def input_parser(self, puzzle_input: str) -> List[str]:
    """Drop whitespace."""
    return [line.replace(" ", "") for line in puzzle_input.split('\n')]

  def solver(self, puzzle_input: list[str], part_one: bool) -> int:
    if part_one:
        # Treat + and * equally.
        conds = [lambda x: x in '+*']
    else:
        # Split on * first making it lower precendent than +.
        conds = [lambda x: x == '*', lambda x: x == '+']
    return sum(self.solve(i, conds) for i in puzzle_input)

  def solve(self, tokens: List[str], f: List[Callable[[str], bool]]) -> int:
    """Tokenize, create tree and math the tree."""
    return self.make_tree(self.tokenize(tokens), f).compute()

  def get_split_for(self, tokens: List[str], conds: List[Callable[[str], bool]]) -> Optional[int]:
    """Return the split-point, respecting (x) as one block."""
    for cond in conds:
      i = len(tokens) - 1
      depth = 0
      while i >= 0:
        if depth == 0 and cond(tokens[i]):
          return i
        if tokens[i] == ')':
          depth += 1
        elif tokens[i] == '(':
          depth -= 1
        i -= 1
    return None

  def make_tree(self, tokens: List[str], conds: List[Callable[[str], bool]]):
    """Build a tree, arbitrary ordering based on the conds."""
    def _go(tkns):
      if len(tkns) == 1:
        return Node(tkns[0])
      # Find the right-most operator and split on that. Treat parens as a block.
      i = self.get_split_for(tkns, conds)
      if i is None:
        # Ran out of tokens. Must be "(exp)".
        assert tkns[0] == '(' and tkns[-1] == ')'
        return _go(tkns[1:-1])
      else:
        left = _go(tkns[:i])
        op = tkns[i]
        right = _go(tkns[i + 1:])
        return Node(left, op, right)
    return _go(tokens)

  def tokenize(self, line: str) -> List[str]:
    """Tokenize the input into strings of nums/+/*/()."""
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
