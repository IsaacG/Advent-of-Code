#!/bin/pypy3

import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List


class Cup:

  def __init__(self, val, prev):
    self.prev = prev
    if prev:
      prev.next = self
    self.next = None
    self.val = val

  def move_next_3(self, other):
    next3 = self.next
    third = self.next.next.next
    self.next = third.next
    self.next.prev = self

    old = other.next
    other.next = next3
    third.next = old

  def next3(self):
    out = []
    cur = self
    for i in range(3):
      cur = cur.next
      out.append(cur.val)
    return out

  def all(self):
    yield self
    c = self.next
    while c != self:
      yield c
      c = c.next

  def __str__(self):
    out = [f'({self.val})']
    c = self.next
    while c != self:
      out.append(str(c.val))
      c = c.next
    return ' '.join(out)
    

class Day23(aoc.Challenge):

  TESTS = (
    aoc.TestCase(inputs='389125467', part=1, want=67384529),
    aoc.TestCase(inputs='389125467', part=2, want=149245887792),
  )

  def solve(self, cups: List[int], rounds: int) -> Cup:
    """Solve the cups game.

    Use a list of labels as a starting point.
    Run for `rounds` iteration.
    Return the cup labeled "1".
    """
    # Build a linked list of Cups with a map from label to Cup.
    mapping = {}
    cur = None
    for i in cups:
      cur = Cup(i, cur)
      mapping[i] = cur

    # Link the last and first cups, making the list circular.
    cur.next = mapping[cups[0]]
    mapping[cups[0]].prev = cur

    
    # Start the game with the "first" Cup.
    cur = mapping[cups[0]]
    highest = max(cups)
    for rounds in range(rounds):
      # Destination label cannot be current or next three labels.
      not_valid = cur.next3() + [cur.val]
      dest = cur.val
      while dest in not_valid:
        # Try one lower value - with circular counting.
        dest = (dest - 1) or highest

      # Move 3 Cups from cur to dest.
      cur.move_next_3(mapping[dest])
      # Move to the next Cup.
      cur = cur.next
    return mapping[1]

  def part2(self, cups: List[int]) -> int:
    """Extend the cups through 1M. Play for 10M rounds."""
    cups = list(cups)
    cups.extend(range(10, int(1e6)+1))
    one = self.solve(cups, int(1e7))
    return one.next.val * one.next.next.val

  def part1(self, cups: List[int]) -> int:
    """Play for 100 rounds, return the list of Cups."""
    cups = list(cups)
    one = self.solve(cups, 100)
    vals = [str(i.val) for i in one.all()][1:]
    return int("".join(vals))

  def preparse_input(self, lines):
    return [int(i) for i in lines[0]]


if __name__ == '__main__':
  Day23().run()

# vim:ts=2:sw=2:expandtab
