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
    direction = 0
    mod = {
      'E': 1, 'N': 1j, 'W': -1, 'S': -1j,
        0: 1,  90: 1j, 180: -1, 270: -1j,
    }
    for l in lines:
      instruction, num = l[0], int(l[1:])
      if instruction in 'NEWS':
        pos += num * mod[instruction]
      if instruction in "LR":
        # R90 == L270
        if instruction == "R":
          num = 360 - num
        # R360 == R0, R(360+n) == R(n)
        direction = (direction + num) % 360
      if instruction == "F":
        pos += num * mod[direction]
    return int(abs(pos.imag) + abs(pos.real))

  def part2(self, lines: List[str]) -> int:
    ship = 0 + 0j
    waypoint = 10 + 1j
    mod = {'E': 1, 'N': 1j, 'W': -1, 'S': -1j}
    for l in lines:
      instruction, num = l[0], int(l[1:])
      if instruction in 'NEWS':
        waypoint += num * mod[instruction]
      if instruction in "LR":
        if instruction == "R":
          num = 360 - num
        for _ in range(0, num, 90):
          waypoint *= 1j
      if instruction == "F":
        ship += num * waypoint
    return int(abs(ship.imag) + abs(ship.real))


if __name__ == '__main__':
  Day12().run()

# vim:ts=2:sw=2:expandtab
