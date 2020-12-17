#!/bin/pypy3

import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List, Tuple

SAMPLE = ["""\
.#.
..#
###
"""]

ACTIVE = '#'
INACTIVE = '.'


class GameOfLifeB:
  """Manage the seating area."""

  def __init__(self, dimensions: int, block: List[str]):
    """Build the board from a list of strings."""
    self.dimensions = dimensions
    self.board = set()
    z = 0
    w = 0
    for y, row in enumerate(block):
      for x, val in enumerate(row):
        if val == ACTIVE:
          self.board.add((w,z,y,x))

  def live_count(self) -> int:
    """Total number of people in the seating area."""
    return len(self.board)

  def active(self, w, z, y, x) -> bool:
    """Return if a spot is active."""
    return (w,z,y,x) in self.board

  def surrounding(self, w, z, y, x) -> int:
    """Count the number of active seats immediately surround this one."""
    return sum(
      True
      for a in (-1,0,1)
      for b in (-1,0,1)
      for c in (-1,0,1)
      for d in (-1,0,1)
      if not (a == 0 and b == 0 and c == 0 and d == 0)
      and self.active(w + d, z + a, y + b, x + c)
    )

  def calc_next(self):
    """Compute the seating area after one iteration."""
    next = set()
    x_min = min(x for (w,z,y,x) in self.board)
    x_max = max(x for (w,z,y,x) in self.board)
    y_min = min(y for (w,z,y,x) in self.board)
    y_max = max(y for (w,z,y,x) in self.board)
    z_min = min(z for (w,z,y,x) in self.board)
    z_max = max(z for (w,z,y,x) in self.board)
    w_min = min(w for (w,z,y,x) in self.board)
    w_max = max(w for (w,z,y,x) in self.board)
    for w in range(w_min - 1, w_max + 2):
      for z in range(z_min - 1, z_max + 2):
        for y in range(y_min - 1, y_max + 2):
          for x in range(x_min - 1, x_max + 2):
            count = self.surrounding(w, z, y, x)
            if self.active(w, z, y, x):
              if count in (2,3):
                next.add((w, z,y,x))
            else:
              if count == 3:
                next.add((w, z,y,x))
    self.board  = next


class GameOfLife:
  """Manage the seating area."""

  def __init__(self, block: List[str]):
    """Build the board from a list of strings."""
    offset = 6
    self.board = {}
    self.next = {}
    z = 0
    for y, row in enumerate(block):
      for x, val in enumerate(row):
        self.board[(z,y,x)] = val
        self.next[(z,y,x)] = INACTIVE

  def print(self):
    x_min = min(x for (z,y,x) in self.board.keys())
    x_max = max(x for (z,y,x) in self.board.keys())
    y_min = min(y for (z,y,x) in self.board.keys())
    y_max = max(y for (z,y,x) in self.board.keys())
    z_min = min(z for (z,y,x) in self.board.keys())
    z_max = max(z for (z,y,x) in self.board.keys())
    for z in range(z_min, z_max+1):
      print(f"z={z}")
      for y in range(y_min, y_max+1):
        line = ""
        for x in range(x_min, x_max+1):
          line += self.board[(z,y,x)]
        print(line)

  def live_count(self) -> int:
    """Total number of people in the seating area."""
    return sum(x == ACTIVE for x in self.board.values())

  def active(self, z, y, x) -> bool:
    """Return if a spot is active."""
    return (z,y,x) in self.board and self.board[(z,y,x)] == '#'

  def inactive(self, y: int, x: int) -> bool:
    """Return if a spot is the inactive."""
    return (z,y,x) in self.board and self.board[(z,y,x)] == '.'

  def surrounding(self, z, y, x) -> int:
    """Count the number of active seats immediately surround this one."""
    return sum(
      True
      for a in (-1,0,1)
      for b in (-1,0,1)
      for c in (-1,0,1)
      if not (a == 0 and b == 0 and c == 0)
      and self.active(z + a, y + b, x + c)
    )

  def calc_next(self):
    """Compute the seating area after one iteration."""
    x_min = min(x for (z,y,x) in self.board.keys())
    x_max = max(x for (z,y,x) in self.board.keys())
    y_min = min(y for (z,y,x) in self.board.keys())
    y_max = max(y for (z,y,x) in self.board.keys())
    z_min = min(z for (z,y,x) in self.board.keys())
    z_max = max(z for (z,y,x) in self.board.keys())
    for z in range(z_min - 1, z_max + 2):
      for y in range(y_min - 1, y_max + 2):
        for x in range(x_min - 1, x_max + 2):
          count = self.surrounding(z, y, x)
          if self.active(z, y, x):
            if count in (2,3):
              self.next[(z,y,x)] = ACTIVE
            else:
              self.next[(z,y,x)] = INACTIVE
          else:
            if count == 3:
              self.next[(z,y,x)] = ACTIVE
            else:
              self.next[(z,y,x)] = INACTIVE
    self.board, self.next = self.next, {}


class Day17(aoc.Challenge):

  TRANSFORM = str

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=112),
    aoc.TestCase(inputs=SAMPLE[0], part=2, want=848),
  )

  def part1(self, lines: List[str]) -> int:
    board = GameOfLife(lines)
    for i in range(6):
      board.calc_next()
    return board.live_count()

  def part2(self, lines: List[str]) -> int:
    board = GameOfLifeB(4, lines)
    for _ in range(6):
      board.calc_next()
    return board.live_count()



if __name__ == '__main__':
  Day17().run()

# vim:ts=2:sw=2:expandtab
