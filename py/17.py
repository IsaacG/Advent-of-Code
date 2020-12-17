#!/bin/pypy3

import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List

SAMPLE = ["""\
.#.
..#
###
"""]

ACTIVE = '#'
INACTIVE = '.'


class SeatingB:
  """Manage the seating area."""

  def __init__(self, block: List[str]):
    """Build the board from a list of strings."""
    offset = 6
    self.board = {}
    self.next = {}
    z = 0
    w = 0
    for y, row in enumerate(block):
      for x, val in enumerate(row):
        self.board[(w,z,y,x)] = val
        self.next[(w,z,y,x)] = INACTIVE

  @classmethod
  def from_str(cls, layout: str) -> "Seating":
    """Seating from `str`."""
    return cls(layout.strip().split('\n'))

  def people_count(self) -> int:
    """Total number of people in the seating area."""
    return sum(x == ACTIVE for x in self.board.values())

  def active(self, w, z, y, x) -> bool:
    """Return if a spot is active."""
    return (w,z,y,x) in self.board and self.board[(w,z,y,x)] == ACTIVE

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
    x_min = min(x for (w,z,y,x) in self.board.keys())
    x_max = max(x for (w,z,y,x) in self.board.keys())
    y_min = min(y for (w,z,y,x) in self.board.keys())
    y_max = max(y for (w,z,y,x) in self.board.keys())
    z_min = min(z for (w,z,y,x) in self.board.keys())
    z_max = max(z for (w,z,y,x) in self.board.keys())
    w_min = min(w for (w,z,y,x) in self.board.keys())
    w_max = max(w for (w,z,y,x) in self.board.keys())
    for w in range(w_min - 1, w_max + 2):
      for z in range(z_min - 1, z_max + 2):
        for y in range(y_min - 1, y_max + 2):
          for x in range(x_min - 1, x_max + 2):
            count = self.surrounding(w, z, y, x)
            if self.active(w, z, y, x):
              if count in (2,3):
                self.next[(w, z,y,x)] = ACTIVE
              else:
                self.next[(w, z,y,x)] = INACTIVE
            else:
              if count == 3:
                self.next[(w, z,y,x)] = ACTIVE
              else:
                self.next[(w, z,y,x)] = INACTIVE
    self.board, self.next = self.next, self.board


class Seating:
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

  @classmethod
  def from_str(cls, layout: str) -> "Seating":
    """Seating from `str`."""
    return cls(layout.strip().split('\n'))

  def people_count(self) -> int:
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
    self.board, self.next = self.next, self.board


class Day17(aoc.Challenge):

  TRANSFORM = str

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=112),
  )

  def part1(self, lines: List[str]) -> int:
    board = Seating(lines)
    for _ in range(6):
      board.calc_next()
    return board.people_count()

  def part2(self, lines: List[str]) -> int:
    board = SeatingB(lines)
    for _ in range(6):
      board.calc_next()
    return board.people_count()



if __name__ == '__main__':
  Day17().run()

# vim:ts=2:sw=2:expandtab
AMPLE = ["""\
.#.
..#
###
""","""\
Before any cycles:

z=0
.#.
..#
###


After 1 cycle:

z=-1
#..
..#
.#.

z=0
#.#
.##
.#.

z=1
#..
..#
.#.


After 2 cycles:

z=-2
.....
.....
..#..
.....
.....

z=-1
..#..
.#..#
....#
.#...
.....

z=0
##...
##...
#....
....#
.###.

z=1
..#..
.#..#
....#
.#...
.....

z=2
.....
.....
..#..
.....
.....


After 3 cycles:

z=-2
.......
.......
..##...
..###..
.......
.......
.......

z=-1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=0
...#...
.......
#......
.......
.....##
.##.#..
...#...

z=1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=2
.......
.......
..##...
..###..
.......
.......
.......
"""]
# vim:ts=2:sw=2:expandtab
