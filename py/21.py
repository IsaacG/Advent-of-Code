#!/bin/pypy3

import aoc
import collections
import itertools
import functools
import math
import re
from typing import Any, Callable, Dict, List

SAMPLE = ["""\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""]


class Day21(aoc.Challenge):

  TRANSFORM = str
  DEBUG = True
  SEP = '\n'

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=5),
    aoc.TestCase(inputs=SAMPLE[0], part=2, want='mxmxvkd,sqjhc,fvjkl'),
  )

  def part2(self, lines: List[str]) -> int:
    solved = {}
    unsolved = set()
    all_ing = []
    candidates = {}
    for line in lines:
      ing, alg = line.split(' (contains ')
      ing = ing.split()
      all_ing.extend(ing)
      alg = alg[:-1].split(', ')

      for i in alg:
        if i not in candidates:
          candidates[i] = set(ing)
        else:
          candidates[i] &= set(ing)
        progress = True
        while any(len(a) == 1 for a in candidates.values()):
          i, j = [(m,n) for m,n in candidates.items() if len(n) == 1][0]
          j = list(j)[0]
          solved[i] = j

          for n in candidates.values():
            if j in n: n.remove(j)


    print(1,candidates)
    print(2,solved)
    good_foods = set(all_ing) - set(solved.values())
    print(3,good_foods)

    progress = True
    while progress:
      progress = False

    bad = ",".join(solved[i] for i in sorted(solved.keys()))

    return bad

  def part1(self, lines: List[str]) -> int:
    solved = {}
    unsolved = set()
    all_ing = []
    candidates = {}
    for line in lines:
      ing, alg = line.split(' (contains ')
      ing = ing.split()
      all_ing.extend(ing)
      alg = alg[:-1].split(', ')

      for i in alg:
        if i not in candidates:
          candidates[i] = set(ing)
        else:
          candidates[i] &= set(ing)
        progress = True
        while any(len(a) == 1 for a in candidates.values()):
          i, j = [(m,n) for m,n in candidates.items() if len(n) == 1][0]
          j = list(j)[0]
          solved[i] = j

          for n in candidates.values():
            if j in n: n.remove(j)


    print(1,candidates)
    print(2,solved)
    good_foods = set(all_ing) - set(solved.values())
    print(3,good_foods)

    progress = True
    while progress:
      progress = False

    return sum(True for i in all_ing if i in good_foods)



  def preparse_input(self, x):
    return x


if __name__ == '__main__':
  Day21().run()

# vim:ts=2:sw=2:expandtab
# vim:ts=2:sw=2:expandtab
