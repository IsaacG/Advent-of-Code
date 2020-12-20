#!/bin/pypy3

import aoc
import collections
import copy
import functools
import math
import re
from typing import Any, Callable, Dict, List

SAMPLE = ["""\
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
""","""
.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###
"""]

MONSTER = [
	'                  # ',
	'#    ##    ##    ###',
	' #  #  #  #  #  #   ',
]

TOP = 0
BOTTOM = 1
LEFT = 2
RIGHT = 3
SIDE_NAMES = {TOP: "TOP", BOTTOM: "BOTTOM", LEFT: "LEFT", RIGHT: "RIGHT"}

def rot90(rows):
  out = []
  for x in range(len(rows[0])):
    r = ''
    for y in range(len(rows) -1, -1, -1):
      r += rows[y][x]
    out.append(r)
  return out

class Tile:

  def __init__(self, block):
    lines = block.split('\n')
    self.num = int(lines[0].split(' ')[1][:-1])
    self.tile_rows = lines[1:]
    # Top, bottom
    edges = [self.tile_rows[0], self.tile_rows[-1]]
    # Left edge
    edges.append([t[0] for t in self.tile_rows])
    # Right edge
    edges.append([t[-1] for t in self.tile_rows])
    # Reversed
    edges.extend([reversed(t) for t in edges])
    # Convert list to str.
    self.edges = [''.join(t) for t in edges]
    self.neighbors = {}

  def is_neighbor(self, other) -> bool:
    return any(e in self.edges for e in other.edges)

  def oriented_edges(self, flipped):
    if flipped:
      return self.edges[4:]
    else:
      return self.edges[:4]

  def top(self):
    return self.edges[0]

  def bottom(self):
    return self.edges[1]

  def left(self):
    return self.edges[2]

  def right(self):
    return self.edges[3]

  def rot90(self):
    self.tile_rows = rot90(self.tile_rows)

  def pair(self, other):
    orient = {TOP: self.top(), BOTTOM: self.bottom(), LEFT: self.left(), RIGHT: self.right()}
    for n, edge in orient.items():
      if edge in other.edges:
        matching_side = n
        matching_edge = edge
        break
    else:
      assert False
    others_side = [i for i, n in enumerate(other.edges) if n == matching_edge][0]

    # Flip other?
    o_edges = other.oriented_edges(others_side > 3)
    if others_side in (4+BOTTOM,4+TOP): # Flip horizontally
      other.tile_rows = ["".join(reversed(i)) for i in other.tile_rows]
    if others_side in (4+LEFT,4+RIGHT): # Flip vertically
      other.tile_rows = list(reversed(other.tile_rows))
    # How to rotate/orient other. 4 combos.
    rotations = [[0,1,2,3],[2,3,1,0],[1,0,3,2],[3,2,0,1]]
    pairings = {TOP:BOTTOM, LEFT:RIGHT, RIGHT:LEFT, BOTTOM:TOP}
    for i, r in enumerate(rotations):
      rotated_edges = [o_edges[n] for n in r]
      if rotated_edges[pairings[matching_side]] == matching_edge:
        other.edges = rotated_edges
        rot_times = i
        break
    else:
      assert False
    for i in range(rot_times):
      other.rot90()
    self.neighbors[matching_side] = other
    other.neighbors[pairings[matching_side]] = self
    # print(f'Pair {self.num} side {SIDE_NAMES[matching_side]} to {other.num} {SIDE_NAMES[pairings[matching_side]]}')

  def trimmed_row(self, row):
    return self.tile_rows[row + 1][1:-1]

  def num_rows(self):
    return len(self.tile_rows) - 2


class Day20(aoc.Challenge):

  TRANSFORM = str
  DEBUG = True
  SEP = '\n\n'

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=20899048083289),
    aoc.TestCase(inputs=SAMPLE[0], part=2, want=SAMPLE[1].strip()),
    # aoc.TestCase(inputs=SAMPLE[0], part=2, want=0)
  )

  def part2(self, blocks: List[str]) -> int:
    tiles = [Tile(b) for b in blocks]
    tiles_by_num = {t.num: t for t in tiles}
    unmatched = list(tiles_by_num.keys())
    matched = [1951]
    while unmatched:
      for tn in list(unmatched):
        found_match = False
        for un in matched:
          t = tiles_by_num[tn]
          u = tiles_by_num[un]
          if t.is_neighbor(u):
            u.pair(t)
            found_match = True
        if found_match:
          unmatched.remove(tn)
          matched.append(tn)
    topleft = tiles[0]

    while 0 in topleft.neighbors or 2 in topleft.neighbors:
      if 0 in topleft.neighbors:
        topleft = topleft.neighbors[0]
      else:
        topleft = topleft.neighbors[2]

    # print("Top left:", topleft.num)
    row_left = topleft
    tile_rows = topleft.num_rows()
    # del topleft.neighbors[BOTTOM]
    final_image = []
    row_count = 0
    while row_left:
      row_count += 1
      subrow = 0
      for i in range(tile_rows):
        subrow += 1
        row_cursor = row_left
        row = ""
        while row_cursor:
          if subrow == 1:
            pass
            # print(row_cursor.num, end=' ')
          row += row_cursor.trimmed_row(i)
          if RIGHT in row_cursor.neighbors:
            row_cursor = row_cursor.neighbors[RIGHT]
          else:
            row_cursor = None
        final_image.append(row)
      if BOTTOM in row_left.neighbors:
        row_left = row_left.neighbors[BOTTOM]
      else:
        row_left = None
      # print()


    # Count monsters in the image
    return '\n'.join(final_image)


  def part1(self, blocks: List[str]) -> int:
    data = {}
    all_edges = []
    for block in blocks:
      lines = block.split('\n')
      tile_num = int(lines[0].split(' ')[1][:-1])
      tile_rows = lines[1:]
      edges = [tile_rows[0], tile_rows[-1]]
      # Left edge
      edges.append([t[0] for t in tile_rows])
      # Right edge
      edges.append([t[-1] for t in tile_rows])
      # Reversed
      edges.extend([reversed(t) for t in edges])
      # Convert list to str.
      edges = [''.join(t) for t in edges]
      all_edges.extend(edges)
      data[tile_num] = edges
    edge_counts = collections.Counter(all_edges)
    return aoc.mult([tile_num for tile_num, edges in data.items() if sum(True for e in edges if edge_counts[e] == 2) == 4])

  def preparse_input(self, x):
    return x


if __name__ == '__main__':
  Day20().run()

# vim:ts=2:sw=2:expandtab
