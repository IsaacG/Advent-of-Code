#!/usr/bin/env python

import typer
from lib import aoc
import collections
import re
from typing import List, Set


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
    aoc.TestCase(inputs=SAMPLE[0], part=2, want=132),  # 20 rounds
    # aoc.TestCase(inputs=SAMPLE[0], part=2, want=2208),  # 100 rounds
  )

  def part2(self, lines: List[List[str]]) -> int:
    """Play Game of Life on a hex grid. See day 17."""
    live = self.build_grid(lines)
    # Speed up tests for convenience.
    limit = 20 if self.testing else 100
    for _ in range(limit):
      # Count all the "neighbor" values.
      counts = collections.Counter(coord + x for x in DIRS for coord in live)

      next_board = set()
      for coord, count in counts.items():
        if count == 2 or (count == 1 and coord in live):
          next_board.add(coord)
      live = next_board

    return len(live)

  def part1(self, lines: List[List[str]]) -> int:
    """Count flipped tiles after applying instructions."""
    return len(self.build_grid(lines))

  def build_grid(self, lines: List[List[str]]) -> Set[complex]:
    """Convert a list of directions to a coord and flip that tile on/off."""
    flipped = set()  # type: Set[complex]
    for line in lines:
      c = sum(DIRMAP[i] for i in line)
      if c in flipped:
        flipped.remove(c)
      else:
        flipped.add(c)
    return flipped

  def parse_input(self, puzzle_input: str):
    """Split lines into lists of directions."""
    dir_re = re.compile('[ns]?[ew]')
    return [dir_re.findall(direction) for direction in puzzle_input.split('\n')]


if __name__ == '__main__':
  typer.run(Day24().run)

# vim:ts=2:sw=2:expandtab
