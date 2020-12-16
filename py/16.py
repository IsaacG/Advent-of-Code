#!/bin/pypy3

import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List

SAMPLE = ["""\
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
""","""
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""]


class Day16(aoc.Challenge):

  TRANSFORM = str
  SEP = '\n\n'

  TESTS = (
    # aoc.TestCase(inputs=SAMPLE[0], part=1, want=71),
    aoc.TestCase(inputs=SAMPLE[1], part=2, want=71),
  )

  def part1(self, chunks: List[str]) -> int:
    rules, yours, near = chunks
    r2 = []
    for line in rules.split('\n'):
       l = line.split(': ')[1]
       r2.append(tuple(tuple(int(p) for p in o.split('-')) for o in l.split(' or ')))
    rules = r2
    r2 = []
    for line in near.split('\n')[1:]:
      r2.append([int(i) for i in line.split(',')])
    near = r2

    bad = 0
    for nums in near:
      bad_val = None
      for num in nums:
        good = False
        for rule in rules:
          for p in rule:
            if p[0] <= num <= p[1]:
              good = True
              break
        if not good:
          bad_val = num
          break
      if bad_val is not None:
        bad += bad_val
    return bad


  def part2(self, chunks: List[str]) -> int:
    rules, yours, near = chunks
    r2 = []
    rule_names = {}
    for line in rules.split('\n'):
       name, l = line.split(': ')
       r2.append(tuple(tuple(int(p) for p in o.split('-')) for o in l.split(' or ')))
       rule_names[name] = tuple(tuple(int(p) for p in o.split('-')) for o in l.split(' or '))
    rules = r2
    r2 = []
    for line in near.split('\n')[1:]:
      r2.append([int(i) for i in line.split(',')])
    near = r2


    good_tickets = []

    bad = 0
    for nums in near:
      bad_val = None
      for num in nums:
        good = False
        for rule in rule_names.values():
          for p in rule:
            if p[0] <= num <= p[1]:
              good = True
              break
        if not good:
          bad_val = num
          break
      if bad_val is not None:
        bad += bad_val
      if bad_val is None:
        good_tickets.append(nums)

    your_ticket = {}
    yours = [int(i) for i in yours.strip().split('\n')[1].split(',')]
    near = good_tickets
    # near.append(yours)
    rules = set(rule_names.keys())
    cols = set(range(len(rules)))
    while rules:
      rule_column = None
      for name in rules:
        valid_columns = []
        for col in cols:
          vals = [n[col] for n in near]
          if all(any(p[0] <= v <= p[1] for p in rule_names[name]) for v in vals):
            valid_columns.append(col)
        if len(valid_columns) == 1:
          break
      if len(valid_columns) == 1:
        your_ticket[name] = yours[valid_columns[0]]
        rules.remove(name)
        cols.remove(valid_columns[0])
        valid_columns = []
    return aoc.mult(v for k, v in your_ticket.items() if k.startswith('departure'))



if __name__ == '__main__':
  Day16().run()

# vim:ts=2:sw=2:expandtab
