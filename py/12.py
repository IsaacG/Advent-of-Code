#!/bin/pypy3

import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List

SAMPLE = ["""\
F10
N3
F7
R90
F11
""", """\
"""]


class Day12(aoc.Challenge):

  TRANSFORM = str
  DEBUG = False

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=25),
    aoc.TestCase(inputs=SAMPLE[0], part=2, want=286),
  )

  def part1(self, lines: List[str]) -> int:
    pos = 0 + 0j
    f = 0
    dE, dN, dW, dS = 0, 90, 180, 270
    mod = {
      'E': 1, 'N': 1j, 'W': -1, 'S': -1j,
        0: 1,  90: 1j, 180: -1, 270: -1j,
    }
    for l in lines:
      i, n = l[0], int(l[1:])
      if i in 'NEWS':
        pos += n * mod[i]
      if i in "LR":
        # R90 == L270
        if i == "R":
          n = 360 - n
        # R360 == R0, R(360+n) == R(n)
        f = (f + n) % 360
      if i == "F":
        pos += n * mod[f]
    return int(abs(pos.imag) + abs(pos.real))

  def part2(self, lines: List[str]) -> int:
    x = 0
    y = 0
    f = 0
    wx = 10
    wy = 1
    for l in lines:
      i, n = l[0], int(l[1:])
      if i == "E":
        wx += n
      if i == "W":
        wx -= n
      if i == "N":
        wy += n
      if i == "S":
        wy -= n
      if i in "LR":
        if i == "R":
          n = 360 - n
        for _ in range(0, n, 90):
          wx, wy = -wy, wx
      if i == "F":
        x += n * wx
        y += n * wy
    return abs(x) + abs(y)


if __name__ == '__main__':
  Day12().run()

# vim:ts=2:sw=2:expandtab
