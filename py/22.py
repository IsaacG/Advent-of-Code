#!/bin/pypy3

import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List

SAMPLE = ["""\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""]
# vim:ts=2:sw=2:expandtab

class Day22(aoc.Challenge):

  SEP = '\n\n'

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=306),
    aoc.TestCase(inputs=SAMPLE[0], part=2, want=291),
  )

  def part1(self, lines: List[str]) -> int:
    p1 = [int(l) for l in lines[0].split('\n')[1:]]
    p2 = [int(l) for l in lines[1].split('\n')[1:]]
    rounds = 0
    while p1 and p2:
      rounds += 1
      cards = p1.pop(0), p2.pop(0)
      assert cards[0] != cards[1]
      if cards[0] > cards[1]:
        p1.append(cards[0])
        p1.append(cards[1])
      else:
        p2.append(cards[1])
        p2.append(cards[0])
    w = p1 if p1 else p2
    w = reversed(w)

    return sum((i+1) * c for i, c in enumerate(w))

  def recurse(self, p1, p2, top=False):
    seen1 = []
    seen2 = []
    rounds = 0
    while p1 and p2:
      rounds += 1

      if p1 in seen1 or p2 in seen2:
        if top:
          w = reversed(p1)
          return sum((i+1) * c for i, c in enumerate(w))
        return 1
      seen1.append(list(p1))
      seen2.append(list(p2))

      cards = p1.pop(0), p2.pop(0)
      assert cards[0] != cards[1]

      winner = None
      # Recursive battle
      if len(p1) >= cards[0] and len(p2) >= cards[1]:
        winner = self.recurse(p1[:cards[0]], p2[:cards[1]])
      else:
        if cards[0] > cards[1]:
          winner = 1
        else:
          winner = 2

      if winner == 1:
        p1.append(cards[0])
        p1.append(cards[1])
      else:
        p2.append(cards[1])
        p2.append(cards[0])
    if top:
      w = p1 if p1 else p2
      w = reversed(w)
      return sum((i+1) * c for i, c in enumerate(w))

    if p1 and not p2:
      return 1
    elif p2 and not p1:
      return 2
    raise RuntimeError

  def part2(self, lines: List[str]) -> int:
    p1 = [int(l) for l in lines[0].split('\n')[1:]]
    p2 = [int(l) for l in lines[1].split('\n')[1:]]
    return self.recurse(p1, p2, top=True)

  def preparse_input(self, x):
    return x


if __name__ == '__main__':
  Day22().run()

# vim:ts=2:sw=2:expandtab
