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
    self.tile_rows = list(reversed(lines[1:]))
    self.neighbors = {}
    self.locked = False

  @property
  def edges(self):
    # Top, bottom
    edges = [self.tile_rows[0], self.tile_rows[-1]]
    # Left edge
    edges.append([t[0] for t in self.tile_rows])
    # Right edge
    edges.append([t[-1] for t in self.tile_rows])
    # Reversed
    edges.extend([reversed(t) for t in edges])
    # Convert list to str.
    return [''.join(t) for t in edges]

  def is_neighbor(self, other) -> bool:
    return any(e in self.edges for e in other.edges)

  def oriented_edges(self, flipped):
    if flipped:
      return self.edges[4:]
    else:
      return self.edges[:4]

  def top(self):
    return self.edges[TOP]

  def bottom(self):
    return self.edges[BOTTOM]

  def left(self):
    return self.edges[LEFT]

  def right(self):
    return self.edges[RIGHT]

  def rot90(self):
    self.tile_rows = rot90(self.tile_rows)

  def pair(self, other):
    orient = {TOP: self.top(), BOTTOM: self.bottom(), LEFT: self.left(), RIGHT: self.right()}
    pairings = {TOP:BOTTOM, LEFT:RIGHT, RIGHT:LEFT, BOTTOM:TOP}
    # How to rotate/orient other. 4 combos.
    rotations = [[0,1,2,3],[2,3,1,0],[1,0,3,2],[3,2,0,1]]

    for n, edge in orient.items():
      if edge in other.edges:
        matching_side = n
        matching_edge = edge
        break
    else:
      assert False
    others_side = [i for i, n in enumerate(other.edges) if n == matching_edge][0]

    self.neighbors[matching_side] = other
    other.neighbors[pairings[matching_side]] = self
    print(f'Pair {self.num} side {SIDE_NAMES[matching_side]} to {other.num} {SIDE_NAMES[pairings[matching_side]]} on o.side {others_side}')
    print(f'Matching {matching_side} to {others_side}')
    rot_map = {
      0: {
        1: (0,0),
        3: (1,0),
        0: (2,1),
        2: (3,0),
      },
      1: {
        0: (0,0),
        2: (1,1),
        1: (2,1),
        3: (3,0),
      },
      2: {
        3: (0,0),
        0: (1,0),
        2: (2,1),
        1: (3,1),
      },
      3: {
        2: (0,0),
        1: (1,0),
        3: (2,1),
        0: (3,1),
      },
    }

    if other.locked:
      return
    other.locked = True

    # Rotate as needed
    flip = False
    o_edges = other.edges[:4]
    for i, r in enumerate(rotations):
      rotated_edges = [o_edges[n] for n in r]
      if rotated_edges[pairings[matching_side]] == matching_edge:
        rot_times = i
        break
      if rotated_edges[pairings[matching_side]] == "".join(reversed(matching_edge)):
        rot_times = i
        flip = True
        break
    else:
      assert False
    print(f'Rot {rot_times}')
    for i in range(rot_times):
      other.rot90()

    # Flip other?
    if flip and matching_side in (TOP, BOTTOM):
      print('V_FLIP')
      other.tile_rows = list(reversed(other.tile_rows))
    if flip and matching_side in (LEFT, RIGHT):
      print('H_FLIP')
      other.tile_rows = ["".join(reversed(i)) for i in other.tile_rows]

  def trimmed_row(self, row):
    return self.tile_rows[row + 1][1:-1]

  def num_rows(self):
    return len(self.tile_rows) - 2


class Day20(aoc.Challenge):

  TRANSFORM = str
  DEBUG = True
  SEP = '\n\n'

  TESTS = (
    # aoc.TestCase(inputs=SAMPLE[0], part=1, want=20899048083289),
    # Validate the stitching.
    # aoc.TestCase(inputs=SAMPLE[0], part=2, want=SAMPLE[1].strip()),
    aoc.TestCase(inputs=SAMPLE[0], part=2, want=273),
    # aoc.TestCase(inputs=SAMPLE[0], part=2, want=0)
  )

  def part2(self, blocks: List[str]) -> int:
    tiles = [Tile(b) for b in blocks]
    tiles_by_num = {t.num: t for t in tiles}
    unmatched = list(tiles_by_num.keys())
    print(unmatched)
    unmatched.remove(1951)
    matched = [1951]
    tiles_by_num[matched[0]].locked = True
    while unmatched:
      progress = False
      for tn in list(unmatched):
        if tn in matched:
          continue
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
          progress = True
      assert progress, unmatched
    topleft = tiles[0]

    while TOP in topleft.neighbors or LEFT in topleft.neighbors:
      if TOP in topleft.neighbors:
        topleft = topleft.neighbors[TOP]
      else:
        topleft = topleft.neighbors[LEFT]

    row_left = topleft
    tile_rows = topleft.num_rows()
    final_image = []
    row_count = 0
    while row_left:
      row_count += 1
      subrow = 0

      row_cursor = row_left
      while row_cursor:
        print(row_cursor.num, end=' ')
        row_cursor = row_cursor.neighbors.get(RIGHT, None)
      print('')
      for i in range(10):
        row_cursor = row_left
        while row_cursor:
          print(row_cursor.tile_rows[i], end=' ')
          row_cursor = row_cursor.neighbors.get(RIGHT, None)
        print('')

      for i in range(tile_rows):
        subrow += 1
        row_cursor = row_left
        row = ""
        while row_cursor:
          if subrow == 1:
            pass
          row_part = row_cursor.trimmed_row(i)
          if RIGHT in row_cursor.neighbors:
            row_cursor = row_cursor.neighbors[RIGHT]
          else:
            row_cursor = None
          row += row_part
        final_image.append(row)
      if BOTTOM in row_left.neighbors:
        assert row_left != row_left.neighbors[BOTTOM]
        row_left = row_left.neighbors[BOTTOM]
      else:
        row_left = None
      print()
    return 0
    return "\n".join(final_image).strip()
    for i, (g, w) in enumerate(zip(final_image, SAMPLE[1].strip().split('\n'))):
      if g != w:
        print(f'Fail line {i} got({g}) want({w})')
    return


    # Count monsters in the image
    count = 0
    for _ in range(2):
      for i in range(4):
        for origin_y in range(len(final_image) - len(MONSTER) + 1):
          for origin_x in range(len(final_image[0]) - len(MONSTER[0]) + 1):
            found = True
            for y in range(len(MONSTER)):
              for x in range(len(MONSTER[0])):
                if MONSTER[y][x] == '#' and final_image[y + origin_y][x + origin_x] != '#':
                  found = False
            if found:
              print(f'Found monster at rot{i} ({origin_y},{origin_x})')
              print('\n'.join(final_image))
              count += 1
              for y in range(len(MONSTER)):
                for x in range(len(MONSTER[0])):
                  if MONSTER[y][x] == '#':
                    l = list(final_image[y + origin_y])
                    l[x + origin_x] = '0'
                    # final_image[y + origin_y] = "".join(l)
        final_image = rot90(final_image)

      final_image = list(reversed(final_image))
    print(f'Monster count: {count}')

    return sum(True for line in final_image for char in line if char == '#')


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
