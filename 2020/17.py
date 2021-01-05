#!/usr/bin/env pypy

import typer
import itertools
from typing import List, Tuple
from lib import aoc

Coord = Tuple[int, ...]

SAMPLE = ["""\
.#.
..#
###
"""]


class GameOfLife:
  """Manage an N-dimensional Conway's Game of Life."""

  ACTIVE = '#'
  INACTIVE = '.'

  def __init__(self, dimensions: int, block: List[str]):
    """Build the board from a 2x2 list of strings."""
    self.dimensions = dimensions
    self.board = set()
    padding = [0] * (dimensions - 2)
    for y, row in enumerate(block):
      for x, val in enumerate(row):
        if val == self.ACTIVE:
          self.board.add(tuple(padding + [y, x]))

    # Compute all possible permutations of neighboring directions.
    self.directions = [
      d for d in itertools.product([-1, 0, 1], repeat=dimensions)
      if not all(i == 0 for i in d)
    ]

  def live_count(self) -> int:
    """Total number of live cells on the board."""
    return len(self.board)

  def active(self, coord: Coord) -> bool:
    """Return if a spot is live."""
    return coord in self.board

  def neighbors(self, coord: Coord) -> List[Coord]:
    """List of all neighboring cells for a given Coord."""
    return [
      tuple(a + b for (a, b) in zip(coord, d))
      for d in self.directions
    ]

  def active_neighbor_count(self, coord: Coord) -> int:
    """Count the number of active seats immediately surround this one.

    We could reuse self.neighbors() here but that's a lot slower.
    """
    return sum(
      True for d in self.directions
      if self.active(tuple(coord[i] + d[i] for i in range(self.dimensions)))
    )

  def calc_next(self):
    """Compute the board after one iteration."""
    next = set()

    potential = set()
    for c in self.board:
      potential.update(self.neighbors(c))
    potential.update(self.board)

    for coord in potential:
      assert isinstance(coord[0], int), coord
      count = self.active_neighbor_count(coord)
      if self.active(coord) and count in (2, 3):
        next.add(coord)
      elif count == 3:
        next.add(coord)
    self.board = next

  def fast_active_neighbor_count(self, coord: Coord) -> int:
    """Fast version of active_neighbor_count. About half the speed, fixed N."""
    w, z, y, x = coord
    return sum(
      True
      for a in (-1, 0, 1)
      for b in (-1, 0, 1)
      for c in (-1, 0, 1)
      for d in (-1, 0, 1)
      if not (a == 0 and b == 0 and c == 0 and d == 0) and (
        self.active((w + d, z + a, y + b, x + c)))
    )

  def fast_calc_next(self):
    """Fast calc_next with fixed N."""
    next = set()

    x_min = min(x for (w, z, y, x) in self.board)
    x_max = max(x for (w, z, y, x) in self.board)
    y_min = min(y for (w, z, y, x) in self.board)
    y_max = max(y for (w, z, y, x) in self.board)
    z_min = min(z for (w, z, y, x) in self.board)
    z_max = max(z for (w, z, y, x) in self.board)
    w_min = min(w for (w, z, y, x) in self.board)
    w_max = max(w for (w, z, y, x) in self.board)
    for w in range(w_min - 1, w_max + 2):
      for z in range(z_min - 1, z_max + 2):
        for y in range(y_min - 1, y_max + 2):
          for x in range(x_min - 1, x_max + 2):
            count = self.fast_active_neighbor_count((w, z, y, x))
            if self.active((w, z, y, x)) and count in (2, 3):
              next.add((w, z, y, x))
            elif count == 3:
              next.add((w, z, y, x))
    self.board = next


class Day17(aoc.Challenge):

  TIMER_ITERATIONS = (5, 2)

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=112),
    aoc.TestCase(inputs=SAMPLE[0], part=2, want=848),
  )

  def solve_game_of_life(self, lines: List[str], dimensions: int) -> int:
    board = GameOfLife(dimensions, lines)
    if dimensions == 4:
      func = board.fast_calc_next
    else:
      func = board.calc_next
    for i in range(6):
      func()
    return board.live_count()

  def part1(self, lines: List[str]) -> int:
    return self.solve_game_of_life(lines, 3)

  def part2(self, lines: List[str]) -> int:
    return self.solve_game_of_life(lines, 4)


if __name__ == '__main__':
  typer.run(Day17().run)

# vim:ts=2:sw=2:expandtab
