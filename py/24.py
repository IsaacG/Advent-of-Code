#!/bin/pypy3

import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List, Set


SAMPLE = ["""\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
"""]

# https://www.redblobgames.com/grids/hexagons/ -- axial coordinates.
# Cartesian coordinates represented by complex numbers, as per Day 12.
DIRMAP = {
  'e': +1 + 0j,
  'w': -1 + 0j,
  'ne': 1 + 1j,
  'nw': 0 + 1j,
  'se': 0 - 1j,
  'sw': -1 - 1j,
}
DIRS = tuple(DIRMAP.values())

class Day24(aoc.Challenge):

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=10),
    aoc.TestCase(inputs=SAMPLE[0], part=2, want=132), # 20 rounds
    # aoc.TestCase(inputs=SAMPLE[0], part=2, want=2208), # 100 rounds
  )

  def part2(self, lines: List[List[str]]) -> int:
    """Play Game of Life on a hex grid. See day 17."""
    live = self.build_grid(lines)
    # Speed up tests for convenience.
    limit = 20 if self.testing else 100
    for _ in range(limit):
      # Compute a set of candidate cells to check.
      neighbors = {l + x for x in DIRS for l in live}
      neighbors.update(live)

      next_board = set()
      for l in neighbors:
        count = sum(True for x in DIRS if l + x in live)
        if l in live and count in (1, 2):
          next_board.add(l)
        elif l not in live and count == 2:
          next_board.add(l)
      live = next_board

    return len(live)

  def part1(self, lines: List[List[str]]) -> int:
    """Count flipped tiles after applying instructions."""
    return len(self.build_grid(lines))

  def build_grid(self, lines: List[List[str]]) -> Set[complex]:
    """Convert a list of directions to a coord and flip that tile on/off."""
    flipped = set()
    for line in lines:
      c = sum(DIRMAP[i] for i in line)
      if c in flipped:
        flipped.remove(c)
      else:
        flipped.add(c)
    return flipped

  def preparse_input(self, x):
    """Split lines into lists of directions."""
    dir_re = re.compile('[ns]?[ew]')
    return [dir_re.findall(l) for l in x]


if __name__ == '__main__':
  Day24().run()

# vim:ts=2:sw=2:expandtab
