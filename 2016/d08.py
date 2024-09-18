#!/bin/python
"""Advent of Code, Day 8: Two-Factor Authentication. Manipulate screen pixels."""

from lib import aoc

SAMPLE = """\
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1"""

InputType = list[str]


class Day08(aoc.Challenge):
    """Day 8: Two-Factor Authentication."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=6),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_re_group_mixed(r".*(rect|row|column)[^\d]+(\d+)[^\d]+(\d+)")

    def solver(self, puzzle_input: InputType, p2: bool) -> int | str:
        width, height = (7, 3) if self.testing else (50, 6)
        grid = [[False] * width for _ in range(height)]

        for line in puzzle_input:
            match line:
                case ["rect", cols, rows]:
                    for row in range(rows):
                        for col in range(cols):
                            grid[row][col] = True
                case ["row", row, distance]:
                    grid[row] = grid[row][-distance:] + grid[row][:-distance]
                case ["column", col, distance]:
                    column = [row[col] for row in grid]
                    for row in range(height):
                        grid[row][col] = column[(row - distance + height) % height]

        if not p2:
            return sum(i for row in grid for i in row)
        return aoc.OCR(grid, validate=p2).as_string()
