#!/usr/bin/env python
"""Day 11. Ferry Seating Area a.k.a. Conway's Game of Life."""

import itertools
from typing import List

from lib import aoc
import data

S1 = data.D11S1
S2 = data.D11S2


DIRECTIONS = [
  (i, j) for i, j in itertools.product((-1, 0, 1), (-1, 0, 1))
  if (i, j) != (0, 0)
]


class Seating:
  """Manage the seating area."""

  def __init__(self, block: List[str]):
    """Build the board from a list of strings."""
    self.board = [[c for c in line] for line in block]
    self.next = [[' ' for c in line] for line in block]
    self.y_max = len(self.board)
    self.x_max = len(self.board[0])
    self.stable = False

  def __eq__(self, other):
    """Seating equality."""
    return isinstance(other, type(self)) and self.board == other.board

  @classmethod
  def from_str(cls, layout: str) -> "Seating":
    """Seating from `str`."""
    return cls(layout.strip().split('\n'))

  def people_count(self) -> int:
    """Total number of people in the seating area."""
    return sum(self.occupied(y, x) for y in range(self.y_max) for x in range(self.x_max))

  def valid(self, y: int, x: int) -> bool:
    """Return if [y,x] are valid coordinates."""
    return (0 <= y < self.y_max) and (0 <= x < self.x_max)

  def occupied(self, y: int, x: int) -> bool:
    """Return if a spot is occupied."""
    return self.valid(y, x) and self.board[y][x] == '#'

  def empty(self, y: int, x: int) -> bool:
    """Return if a spot is an empty seat."""
    return self.valid(y, x) and self.board[y][x] == 'L'

  def floor(self, y: int, x: int) -> bool:
    """Return if a spot is the floor."""
    return self.valid(y, x) and self.board[y][x] == '.'

  def surrounding(self, y: int, x: int) -> int:
    """Count the number of occupied seats immediately surround this one."""
    return sum(
      self.occupied(y + i, x + j)
      for i, j in DIRECTIONS
    )

  def visible(self, y: int, x: int) -> int:
    """Count the number of occupied seats visible from one."""
    count = 0
    for i, j in DIRECTIONS:
      c_x = x + i
      c_y = y + j
      while self.valid(c_y, c_x):
        if self.occupied(c_y, c_x):
          count += 1
        if self.occupied(c_y, c_x) or self.empty(c_y, c_x):
          break
        c_x += i
        c_y += j
    return count

  def calc_next(self, threshold, counting):
    """Compute the seating area after one iteration."""
    for y in range(self.y_max):
      for x in range(self.x_max):
        if self.floor(y, x):
          self.next[y][x] = '.'
          continue
        count = counting(y, x)
        if self.empty(y, x) and count == 0:
          self.next[y][x] = '#'
        elif self.occupied(y, x) and count >= threshold:
          self.next[y][x] = 'L'
        else:
          self.next[y][x] = self.board[y][x]
    if self.board == self.next:
      self.stable = True
    self.board, self.next = self.next, self.board


class Day11(aoc.Challenge):
  """Solve Day 11."""

  TESTS = [
    aoc.TestCase(inputs=S1[0], part=1, want=37),
    aoc.TestCase(inputs=S2[0], part=2, want=26),
  ]
  TIMEOUT = 60

  def pre_run(self, *args, **kwargs):
    """Walk through the examples, frame by frame, and validate."""
    self.debug('Validate frames.')
    board = Seating.from_str(S1[0])
    for want in S1:
      assert board == Seating.from_str(want)
      board.calc_next(4, board.surrounding)

    board = Seating.from_str(S2[0])
    for want in S2:
      assert board == Seating.from_str(want)
      board.calc_next(5, board.visible)

  def solution(self, board: Seating, threshold: int, counting) -> int:
    """Solve for a board."""
    while not board.stable:
      board.calc_next(threshold, counting)
    return board.people_count()

  def part1(self, puzzle_input: List[str]) -> int:
    board = Seating(puzzle_input)
    return self.solution(board, 4, board.surrounding)

  def part2(self, puzzle_input: List[str]) -> int:
    board = Seating(puzzle_input)
    return self.solution(board, 5, board.visible)
