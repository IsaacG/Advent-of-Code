#!/bin/python
"""Advent of Code, Day 8: Two-Factor Authentication. Manipulate screen pixels."""

from lib import aoc

PARSER = aoc.parse_re_group_mixed(r".*(rect|row|column)[^\d]+(\d+)[^\d]+(\d+)")


def solve(data: list[str], part: int, testing: bool) -> int | str:
    """Return what is on the screen after toggling pixels."""
    width, height = (7, 3) if testing else (50, 6)
    grid = [[False] * width for _ in range(height)]

    for line in data:
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

    if part == 1:
        return sum(i for row in grid for i in row)
    return aoc.OCR(grid, validate=True).as_string()


SAMPLE = """\
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1"""
TESTS = [(1, SAMPLE, 6)]
