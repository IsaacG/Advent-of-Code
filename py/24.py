#!/bin/pypy3

import aoc
import collections
import functools
import math
import re
from typing import Any, Callable, Dict, List


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

DIR = (1,-1,1j, -1j, 1+1j, -1-1j)

class Day24(aoc.Challenge):

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=10),
    aoc.TestCase(inputs=SAMPLE[0], part=2, want=2208),
  )

  def part2(self, lines: List[str]) -> int:
    flipped = self.build_grid(lines)
    live = {k for k, v in flipped.items() if v}
    for _ in range(100):
      neighbors = set(live)
      next_board = set()
      for l in live:
        neighbors.update((l + x for x in DIR))
      for l in neighbors:
        count = sum(True for x in DIR if l + x in live)
        if l in live and count in (1,2):
          next_board.add(l)
        elif l not in live and count == 2:
          next_board.add(l)
      live = next_board

    return len(live)

  def part1(self, lines: List[str]) -> int:
    flipped = self.build_grid(lines)
    return sum(flipped.values())

  def build_grid(self, lines):
    flipped = collections.defaultdict(lambda: False)
    for line in lines:
      c = 0 + 0j
      for i in line:
        if i == 'e':
          c += (1 + 0j)
        elif i == 'w':
          c -= (1 + 0j)
        elif i == 'ne':
          c += (1 + 1j)
        elif i == 'nw':
          c += (0 + 1j)
        elif i == 'se':
          c -= (0 + 1j)
        elif i == 'sw':
          c -= (1 + 1j)
      flipped[c] = not flipped[c]
    return flipped

  def preparse_input(self, x):
    out = []
    for l in x:
      row = []
      l = list(l)
      while l:
        if l[0] in 'ew':
          row.append(l.pop(0))
        else:
          row.append(l[0] + l[1])
          l.pop(0)
          l.pop(0)
      out.append(row)
    return out


if __name__ == '__main__':
  Day24().run()

# vim:ts=2:sw=2:expandtab
