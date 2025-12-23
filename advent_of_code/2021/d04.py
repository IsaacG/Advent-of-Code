#!/bin/python
"""Advent of Code: Day 04. Undersea Bingo with a giant squid."""


class BingoCard:
    """A Bingo card.

    Store Bingo boards as list[list[int|None]], swapping out numbers for None
    when they are crossed out.
    """

    def __init__(self, chunk: str):
        self.rows: list[list[int | None]] = [
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


def solve(data: tuple[list[int], list[BingoCard]], part: int) -> int:
    """Simulate a game of Bingo."""
    inputs, boards = data
    for ball in inputs:
        for board in boards:
            board.update(ball)
            if part == 1 and board.won():
                return ball * int(board)
        if len(boards) > 1:
            boards = [b for b in boards if not b.won()]
        elif boards[0].won():
            return ball * int(boards[0])
    raise RuntimeError("no winner found")


def input_parser(data: str) -> tuple[list[int], list[BingoCard]]:
    """Parse the input data."""
    chunks = data.split("\n\n")
    inputs = [int(i) for i in chunks[0].split(",")]
    boards = [BingoCard(chunk) for chunk in chunks[1:]]
    return inputs, boards


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
TESTS = [(1, SAMPLE, 4512), (2, SAMPLE, 1924)]
