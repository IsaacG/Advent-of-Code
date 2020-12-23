#!/bin/pypy3

import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List


class Node:

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

  TRANSFORM = str
  DEBUG = True
  SEP = '\n'

  TESTS = (
    aoc.TestCase(inputs='389125467', part=1, want='67384529'),
    aoc.TestCase(inputs='389125467', part=2, want=149245887792),
  )

  def part2(self, lines: List[str]) -> int:
    cups = [int(i) for i in lines[0]]
    cups.extend(range(10,1000001))
    first = Node(cups.pop(0), None)
    cur = first
    for i in cups:
      cur = Node(i, cur)
    cur.next = first
    first.prev = cur
    mapping = {n.val: n for n in first.all()}

    cur = first
    for rounds in range(10000000):
      take = cur.next3()
      dest = (cur.val - 1) or 1000000
      while dest in take:
        dest = (dest - 1) or 1000000

      dest = mapping[dest]
      cur.move_next_3(dest)
      cur = cur.next
    one = mapping[1]
    return one.next.val * one.next.next.val


  def part1(self, lines: List[str]) -> int:
    cups = [int(i) for i in lines[0]]
    l = len(cups)
    cur = 0
    for rounds in range(100):
      print(f'-- move {rounds+1} --')
      print(f'cups: {cups}')
      current = cups[cur % l]
      print('current:', current)
      take = [cups[(cur + j) % l] for j in (1,2,3)]
      print(f'pick up: {take}')
      for i in range(3):
        try:
          del cups[(cur+1)]
        except:
          del cups[0]
      print(cups)
      smaller = [i for i in cups if i < current]
      if rounds == 8:
        print('smaller', smaller)
      if smaller:
        dest_v = max(smaller)
      else:
        dest_v = max(cups)
      print(f'destination: {dest_v}')
      dest = (cups.index(dest_v) + 1) % l
      cups.insert(dest, take[2])
      cups.insert(dest, take[1])
      cups.insert(dest, take[0])
      cur = (cups.index(current) + 1) % l
      print('1', current, cur, cups[cur])
    print(cups)
    return "".join(str(i) for i in (cups[1+cups.index(1):] + cups[:cups.index(1)]))

  def preparse_input(self, x):
    return x


if __name__ == '__main__':
  Day23().run()

# vim:ts=2:sw=2:expandtab
