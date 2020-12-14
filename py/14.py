#!/bin/python

import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List

SAMPLE = ["""\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""","""\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""]


class Day14(aoc.Challenge):

  TRANSFORM = str
  DEBUG = True

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=165),
    aoc.TestCase(inputs=SAMPLE[1], part=2, want=208),
  )

  def part1(self, lines: List[str]) -> int:
    mem = {}
    mask = 0
    for line in lines:
      op, _, val = line.split()
      if op == 'mask':
        mask = val
      else:
        addr = op[4:-1]
        mem[int(addr)] = self.masked(mask, int(val))
    return sum(mem.values())

  def masked(self, m, v):
    m0 = int(m.replace('X', '0'), 2)
    m1 = int(m.replace('X', '1'), 2)
    u = v
    u = u | m0
    u = u & m1
    return u


  def part2(self, lines: List[str]) -> int:
    mem = {}
    mask = 0
    for line in lines:
      op, _, val = line.split()
      if op == 'mask':
        mask = val
      else:
        addr = int(op[4:-1])
        val = int(val)
        print(val)
        for e in self.expand(mask, addr):
          print(e)
          mem[e] = val
        print('===')

    return sum(mem.values())

  def expand(self, mask, addr):
    addr = f'{addr:036b}'
    # print(mask)
    # print(addr)
    out = ''
    for a, b in zip(mask, addr):
      if a == '0':
        out += b
      if a == '1':
        out += '1'
      if a == 'X':
        out += 'X'
    # print(out)

    expanded = []
    l = sum(True for i in out if i == 'X')
    # print('Count:', l)
    for i in range(2**l):
      add2 = list(out)
      aply = format(i, ('0%db' % l))
      # print(aply)
      # print("".join(add2))
      for char in aply:
        add2[add2.index('X')] = char
      expanded.append(int("".join(add2), 2))
    return expanded
    


if __name__ == '__main__':
  Day14().run()

# vim:ts=2:sw=2:expandtab
