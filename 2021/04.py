#!/bin/python

"""Advent of Code: Day 04."""

import collections
import functools
import math
import re
import typer
from typing import Any, Callable

from lib import aoc

SAMPLE = ["""\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""]


class Day04(aoc.Challenge):

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=4512),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=1924),
    )

    # Convert lines to type:
    # INPUT_TYPES = int
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def is_done(self,board):
      return any(all(elem is None for elem in row) for row in board) or (
        any(all(row[i] is None for row in board) for i in range(len(board[0]))))

    def part2(self, lines: list[str]) -> int:
        inputs = lines[0]
        boards = [
          [[int(elem) for elem in row.split()] for row in chunk.splitlines()]
          for chunk in lines[1:]
        ]
        for num in inputs.split(","):
          num = int(num)
          for board in boards:
            for row in board:
              for i in range(len(row)):
                if row[i] == num:
                  row[i] = None
          if len(boards) > 1:
            boards = [b for b in boards if not self.is_done(b)]
          if len(boards) == 1 and self.is_done(boards[0]):
            break
        board = boards[0]
        print(num)
        print(sum(ele for row in board for ele in row if ele))
        return int(num) * sum(ele for row in board for ele in row if ele)

    def part1(self, lines: list[str]) -> int:
        inputs = lines[0]
        boards = [
          [[int(elem) for elem in row.split()] for row in chunk.splitlines()]
          for chunk in lines[1:]
        ]
        winner = None
        for num in inputs.split(","):
          num = int(num)
          for board in boards:
            for row in board:
              for i in range(len(row)):
                if row[i] == num:
                  row[i] = None
            if any(all(elem is None for elem in row) for row in board) or (
              any(all(row[i] is None for row in board) for i in range(len(board[0])))):
              print(board)
              winner = board
              break
          if winner: break
        print(num)
        print(sum(ele for row in board for ele in row if ele))
        return int(num) * sum(ele for row in board for ele in row if ele)

    def parse_input(self, puzzle_input: str):
        """Parse the input data."""
        return puzzle_input.split('\n\n')

if __name__ == '__main__':
    typer.run(Day04().run)
