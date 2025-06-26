#!/bin/python
"""Advent of Code: Day 04."""

from typing import Optional

from lib import aoc

SAMPLE = """\
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
"""


class BingoCard:
    """A Bingo card."""

    def __init__(self, chunk: str):
        self.rows: list[list[Optional[int]]] = [
            [int(elem) for elem in row.split()]
            for row in chunk.splitlines()
        ]
        self.width = len(self.rows[0])

    def won(self) -> bool:
        """Return if this card is a winner."""
        # Check for a row.
        if any(all(elem is None for elem in row) for row in self.rows):
            return True
        # Check for a column.
        if any(all(row[i] is None for row in self.rows) for i in range(self.width)):
            return True
        return False

    def update(self, num: int) -> None:
        """Update the card, crossing off a number."""
        for row in self.rows:
            for i in range(self.width):
                if row[i] == num:
                    row[i] = None

    def __int__(self):
        """Return the int-value of the card (sum of all non-used numbers)."""
        return sum(elem for row in self.rows for elem in row if elem)


InputType = tuple[list[int], list[BingoCard]]


class Day04(aoc.Challenge):
    """Undersea Bingo with a giant squid.

    Store Bingo boards as list[list[int|None]], swapping out numbers for None
    when they are crossed out.
    """

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=4512),
        aoc.TestCase(inputs=SAMPLE, part=2, want=1924),
    )

    def part1(self, puzzle_input: InputType) -> int:
        """Find the first winning Bingo card."""
        inputs, boards = puzzle_input
        for ball in inputs:
            for board in boards:
                board.update(ball)
                if board.won():
                    return ball * int(board)
        raise RuntimeError("no winner found")

    def part2(self, puzzle_input: InputType) -> int:
        """Find the last winning Bingo card."""
        inputs, boards = puzzle_input
        for ball in inputs:
            for board in boards:
                board.update(ball)
            if len(boards) > 1:
                boards = [b for b in boards if not b.won()]
            elif boards[0].won():
                return ball * int(boards[0])
        raise RuntimeError("no winner found")

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        chunks = puzzle_input.split("\n\n")
        inputs = [int(i) for i in chunks[0].split(",")]
        boards = [BingoCard(chunk) for chunk in chunks[1:]]
        return inputs, boards
