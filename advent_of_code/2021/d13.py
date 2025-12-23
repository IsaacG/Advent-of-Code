#!/bin/python
"""Advent of Code: Day 13. Fold a piece of transparent paper a bunch of times to reveal a pattern."""
from lib import aoc


def fold(points: set[complex], axis: str, position: int) -> set[complex]:
    """Fold the sheet along an axis."""
    new = set()
    for point in points:
        if axis == "y":
            if point.imag < position:
                new.add(point)
            else:
                new.add(point.real + (2 * position - point.imag) * 1j)
        if axis == "x":
            if point.real < position:
                new.add(point)
            else:
                new.add(2 * position - point.real + point.imag * 1j)
    return new


def solve(data: tuple[set[complex], list[tuple[str, int]]], part: int) -> int:
    """Fold the sheet many times and render the resulting points."""
    points, instructions = data
    for axis, position in instructions:
        points = fold(points, axis, position)
        if part == 1:
            # Count the points after one fold.
            return len(points)

    # The actual solution requires OCR or visual reading.
    return aoc.OCR.from_point_set(points).as_string()


def input_parser(data: str) -> tuple[set[complex], list[tuple[str, int]]]:
    """Parse the input data."""
    # Dots on the top half, instructions below.
    dots, instructions = data.split("\n\n")
    # Dots become (x,y) points as complex values.
    points = set()
    for line in dots.splitlines():
        x_pos, y_pos = line.split(",")
        points.add(int(x_pos) + int(y_pos) * 1j)

    # Folds are an axis and offset.
    folds = []
    for line in instructions.splitlines():
        instruction = line.split()[-1]
        axis, position = instruction.split("=")
        folds.append((axis, int(position)))
    return points, folds


SAMPLE = """\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""
TESTS = [(1, SAMPLE, 17)]
