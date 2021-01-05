#!/usr/bin/env pypy
"""Day 20. Process satellite images."""

import typer
from lib import aoc
import collections
import enum
from typing import Dict, List, Tuple
import data

# An image row/column/edge is a list of chars. An image is a list of these.
Row = List[str]
Image = List[Row]

SAMPLE = data.D20
MONSTER = data.D20_MONSTER


class Side(enum.IntEnum):
  """A tile side."""
  TOP = 0
  RIGHT = 1
  BOTTOM = 2
  LEFT = 3

  def neighbor(self: 'Side') -> 'Side':
    """Return the neighboring Side of a connected Tile.

    Map TOP <=> BOTTOM, RIGHT <=> LEFT.
    """
    return Side((4 + self.value - 2) % 4)


def rot90(rows: Image) -> Image:
  """Rotate an Image by 90 degrees.

  Return a list of rows where each output row is a reversed input column.

  a b c      d a
  d e f  =>  e b
             f c
  """
  return [
    list(reversed(
      [rows[y][x] for y in range(len(rows))]
    ))
    for x in range(len(rows[0]))
  ]


class Tile:
  """An image tile, a part of the whole."""

  def __init__(self, block: str):
    """Construct a Tile from the input text."""
    lines = block.split('\n')
    self.num = int(lines[0].split(' ')[1][:-1])
    self.image = [list(line) for line in lines[1:]]
    # Neighboring tiles for stitching.
    self.neighbors = {}  # type: Dict[Row, Tile]
    # Used to verify we don't try to rotate a tile multiple times.
    # Not needed to solve AOC.
    self.oriented = False

  def edges(self) -> List[Row]:
    """Return a list of edges. Top, right, bottom left."""
    return [
      self.image[0],
      self.col(-1),
      self.image[-1],
      self.col(0),
    ]

  def all_edges(self) -> List[Row]:
    """Return all edges, i.e. edges plus their flipped version."""
    edges = self.edges()
    edges.extend([list(reversed(t)) for t in edges])
    return edges

  def edge(self, side: Side) -> Row:
    """Return a specific edge of the image."""
    return self.edges()[side.value]

  def col(self, n: int) -> Row:
    """Return an column from the image."""
    return [t[n] for t in self.image]

  def is_neighbor(self, other: 'Tile') -> bool:
    """Check if these Tiles are neighbors, i.e. share a common Edge."""
    assert isinstance(other, type(self))
    return any(e in self.edges() for e in other.all_edges())

  def rot90(self, count: int):
    """Rotate self.image by count * 90 degrees."""
    for _ in range(count % 4):
      self.image = rot90(self.image)

  def _common_edge(self, other) -> Tuple[Row, Side]:
    """Find the common edge between two Tiles."""
    other_edges = other.all_edges()
    for n, edge in enumerate(self.edges()):
      if edge in other_edges:
        return edge, Side(n)
    else:
      assert False, f'Failed to find a matching edge between {self.num} and {other.num}'

  def _orient(self, other):
    """Orient the other tile to align with this tile."""
    matching_edge, matching_side = self._common_edge(other)
    want_others_side = matching_side.neighbor()

    got_others_side = Side([
      i for i, n in enumerate(other.all_edges())
      if n == matching_edge
    ][0] % 4)  # mod 4 to ignore if it is a regular or flipped edge.

    rotations_needed = 4 + want_others_side - got_others_side
    other.rot90(rotations_needed)
    # Maybe flip.
    if other.edge(matching_side.neighbor()) != matching_edge:
      if matching_side in (Side['TOP'], Side['BOTTOM']):
        other.h_flip()
      else:
        other.v_flip()

  def pair(self, other):
    """Pair up two tiles."""
    matching_edge, matching_side = self._common_edge(other)

    # Link the tiles to each other.
    self.neighbors[matching_side] = other
    other.neighbors[matching_side.neighbor()] = self
    # print(f'Pair {self.num} side {matching_side} to {other.num}.')

    if not other.oriented:
      self._orient(other)
      other.oriented = True

  def h_flip(self):
    """Flip horizontally."""
    self.image = [list(reversed(i)) for i in self.image]

  def v_flip(self):
    """Flip vertically."""
    self.image = list(reversed(self.image))

  def trimmed_row(self, row: int) -> Row:
    """Return a row of the image, ignoring the edges."""
    return self.image[row + 1][1:-1]

  def num_rows(self):
    """Return the number of rows in the image - ignoring edges."""
    return len(self.image) - 2


class Day20(aoc.Challenge):
  """Stitch image tiles and find sea monsters in them."""

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=20899048083289),
    aoc.TestCase(inputs=SAMPLE[0], part=2, want=273),
  )

  def stitched_tiles(self, blocks: List[str]) -> Dict[int, Tile]:
    """Turn input into a set of Tiles stitched together."""
    tiles = {t.num: t for t in [Tile(b) for b in blocks]}

    # Use idea by leftylink to build a map of Edge => Tile.
    # Use that map to quickly find adjacent Tiles to connect.
    edge_to_tile = collections.defaultdict(list)
    for tile in tiles.values():
      for e in tile.all_edges():
        edge_to_tile[''.join(e)].append(tile)

    # Maintain a queue of discovered Tiles to place, seeded with an arbitrary Tile.
    to_process = set([list(tiles.values()).pop()])
    # Already placed Tiles that should not be re-queued.
    already_processed = set()

    while to_process:
      tile = to_process.pop()
      already_processed.add(tile)
      # For all edges, find, pair and process neighbors.
      for edge in tile.edges():
        edge = ''.join(edge)
        # No neighbors. This edge is at the edge of the image.
        if len(edge_to_tile[edge]) == 1:
          continue
        other = [i for i in edge_to_tile[edge] if i != tile][0]
        tile.pair(other)
        if other not in already_processed:
          to_process.add(other)

    return tiles

  def find_corner(self, tiles: Dict[int, 'Tile'], dirs: List[Side]) -> int:
    """Find a corner tile in a stitched set of tiles.

    Start at any arbitrary tile and walk all the way in two directions.
    """
    cur = list(tiles.values())[0]
    for d in dirs:
      while d in cur.neighbors:
        if d in cur.neighbors:
          cur = cur.neighbors[d]
    return cur.num

  def stitched_image(self, tiles: Dict[int, Tile]) -> Image:
    """Return the stitched image from the tiles."""
    image = []

    # Start at the top left and work our way down the tiles.
    #  For each image line, walk tiles from left to right to generate full row.
    row_left = tiles[self.find_corner(tiles, (Side['TOP'], Side['LEFT']))]
    while row_left:
      for i in range(row_left.num_rows()):
        row = []
        row_cursor = row_left
        while row_cursor:
          # Add this tile's piece to the complete row and shift right.
          row.extend(row_cursor.trimmed_row(i))
          row_cursor = row_cursor.neighbors.get(Side['RIGHT'])
        # Add the new row to the overall image.
        image.append(row)
      # Shift down.
      row_left = row_left.neighbors.get(Side['BOTTOM'])

    return image

  def part2(self, blocks: List[str]) -> int:
    """Return how choppy the waters are.

    Stitch tiles. Build image. Locate sea monsters. Replace with 0's. Count remaining #'s.
    """
    tiles = self.stitched_tiles(blocks)

    image = self.stitched_image(tiles)
    # Check I generate the correct stitched image.
    if self.testing:
      assert '\n'.join(''.join(line) for line in image) == SAMPLE[1].strip()

    # Count monsters in the image
    monster_count = 0
    monster_orientation = set()
    # For all flips, for all rotations, look for monsters.
    for j in range(2):
      for i in range(4):
        # Check if a monster exists at all coordinates.
        for origin_y in range(len(image) - len(MONSTER) + 1):
          for origin_x in range(len(image[0]) - len(MONSTER[0]) + 1):
            # Test if a monster lives at this spot.
            found = True
            for y in range(len(MONSTER)):
              for x in range(len(MONSTER[0])):
                if MONSTER[y][x] == '#' and image[y + origin_y][x + origin_x] != '#':
                  found = False
                  break
              if not found:
                break
            if found:
              self.debug(f'Found monster at rot{i} flips{j} ({origin_y},{origin_x})')
              monster_orientation.add(f'{i}.{j}')
              monster_count += 1
              # Redraw the monster using 0's.
              for y in range(len(MONSTER)):
                for x in range(len(MONSTER[0])):
                  if MONSTER[y][x] == '#':
                    image[y + origin_y][x + origin_x] = '0'
        if monster_count:
          break
        # Rotate and try again.
        image = rot90(image)
      if monster_count:
        break
      # Flip and try again.
      image = list(reversed(image))
    self.debug(f'Monster count: {monster_count}')

    # Monsters ought to only appear when the image is held a specific way.
    assert len(monster_orientation) == 1
    if self.testing:
      assert monster_count == 2

    # Count the waves.
    return sum(True for line in image for char in line if char == '#')

  def part1(self, blocks: List[str]) -> int:
    """Return the product of the four corner tiles' numbers."""
    tiles = self.stitched_tiles(blocks)

    # Four corners. Top left, top right, bottom left, bottom right.
    line = list(range(4))
    corners = zip(line, line[1:] + line[:1])
    return self.mult(
      self.find_corner(tiles, corner)
      for corner in corners
    )

  def parse_input(self, puzzle_input: str):
    return puzzle_input.split('\n\n')


if __name__ == '__main__':
  typer.run(Day20().run)

# vim:ts=2:sw=2:expandtab
