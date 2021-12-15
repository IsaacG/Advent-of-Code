#!/bin/python
"""Advent of Code: Day 13."""

import typer

from lib import aoc

InputType = tuple[set[complex], list[tuple[str, int]]]
SAMPLE = ["""\
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
"""]


class Day13(aoc.Challenge):
    """Fold a piece of transparent paper a bunch of times to reveal a pattern."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=17),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=64), # Not really, but I don't OCR.
    )

    @staticmethod
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

    def part1(self, lines: InputType) -> int:
        """Fold the sheet once and count points."""
        points, instructions = lines
        axis, position = instructions[0]
        points = self.fold(points, axis, position)
        return len(points)

    def part2(self, lines: InputType) -> int:
        """Fold the sheet many times and render the resulting points."""
        points, instructions = lines
        for axis, position in instructions:
            points = self.fold(points, axis, position)
        # TODO: Can we do all the folds in a single pass?

        # The actual solution requires OCR or visual reading.
        self.debug(aoc.render(points))
        # Since I do not have an OCR, return an arbitrary number.
        return sum(int(point.real * point.imag) for point in points)

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        # Dots on the top half, instructions below.
        dots, instructions = puzzle_input.split("\n\n")
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


if __name__ == "__main__":
    typer.run(Day13().run)

# vim:expandtab:sw=4:ts=4
