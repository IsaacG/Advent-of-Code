#!/bin/python

import aoc
from typing import List

S1 = ["""\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
""", """\
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
""", """\
#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
""", """\
#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##
""", """\
#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##
""", """\
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
"""]

S2 = ["""\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
""", """\
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
""", """\
#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#
""", """\
#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#
""", """\
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#
""", """\
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
""", """\
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
"""]


class Seating:

  def __init__(self, block: List[str]):
    self.board = [[c for c in line] for line in block]
    self.y_max = len(self.board)
    self.x_max = len(self.board[0])

  def __eq__(self, other):
    return type(self) == type(other) and self.board == other.board

  @classmethod
  def from_str(cls, s):
    return cls(s.strip().split('\n'))

  def people_count(self):
    return sum(1 for row in self.board for i in row if i == '#')

  def valid(self, y, x):
    return (0 <= y < self.y_max) and (0 <= x < self.x_max)

  def occupied(self, y, x):
    if self.valid(y, x) and self.board[y][x] == '#':
      return 1

  def surrounding(self, y, x):
    c = 0
    for i in (-1, 0, 1):
      for j in (-1, 0, 1):
        if i == 0 and j == 0:
          continue
        if self.occupied(y + i, x + j):
          c += 1
    return c

  def visible(self, y, x):
    c = 0
    for i in (-1, 0, 1):
      for j in (-1, 0, 1):
        if i == 0 and j == 0:
          continue
        c_x = x + i
        c_y = y + j
        while self.valid(c_y, c_x):
          if self.occupied(c_y, c_x):
            c += 1
            break
          if self.board[c_y][c_x] == 'L':
            break
          c_x += i
          c_y += j
    return c

  def next_board(self, part):
    threshold = {1: 4, 2: 5}[part]
    counting = {1: self.surrounding, 2: self.visible}[part]
    n = []
    for y in range(self.y_max):
      row = ''
      for x in range(self.x_max):
        if self.board[y][x] == '.':
          row += '.'
          continue
        count = counting(y, x)
        if self.board[y][x] == 'L' and count == 0:
          row += '#'
        elif self.occupied(y, x) and count >= threshold:
          row += 'L'
        else:
          row += self.board[y][x]
      n.append(row)
    return type(self)(n)

  
class Day11(aoc.Challenge):

  TRANSFORM = str
  DEBUG = True

  TESTS = (
    aoc.TestCase(inputs=S1[0], part=1, want=37),
    aoc.TestCase(inputs=S2[0], part=2, want=26),
  )

  def algo(self, lines: List[str], testing: bool, part: int) -> int:
    if testing:
      test_data = {1: S1, 2: S2}[part]
      board = Seating(lines)
      for i in range(len(S1)):
        assert board == Seating.from_str(test_data[i])
        board = board.next_board(part=part)

    board = None
    new_board = Seating(lines)
    while new_board != board:
      board = new_board
      new_board = board.next_board(part=part)

    return board.people_count()
    
  def part1(self, lines: List[str], testing: bool = False) -> int:
    return self.algo(lines, testing, 1)

  def part2(self, lines: List[str], testing: bool = False) -> int:
    return self.algo(lines, testing, 2)


if __name__ == '__main__':
  Day11().run()

# vim:ts=2:sw=2:expandtab
