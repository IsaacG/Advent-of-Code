#!/bin/python
"""Advent of Code: Day 13."""

import collections
import functools
import math
import re

import typer

from lib import aoc

InputType = list[int]
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

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=17),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=0),
    )

    # Convert lines to type:
    INPUT_TYPES = int
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, lines: InputType) -> int:
        points, instructions = lines
        for axis, pos in instructions:
            new = set()
            if axis == "y":
                for point in points:
                    if point.imag < pos:
                        new.add(point)
                    else:
                        new.add(point.real + (pos - (int(point.imag) - pos)) * 1j)
            if axis == "x":
                for point in points:
                    if point.real < pos:
                        new.add(point)
                    else:
                        new.add((pos - (int(point.real) - pos)) + int(point.imag) * 1j)
            break
        return len(new)

    def part2(self, lines: InputType) -> int:
        points, instructions = lines
        for axis, pos in instructions:
            new = set()
            if axis == "y":
                for point in points:
                    if point.imag < pos:
                        new.add(point)
                    else:
                        new.add(point.real + (pos - (int(point.imag) - pos)) * 1j)
            if axis == "x":
                for point in points:
                    if point.real < pos:
                        new.add(point)
                    else:
                        new.add(int(pos - (int(point.real) - pos)) + int(point.imag) * 1j)
            print("inst", axis, pos)
            points = new
            xs = max(int(p.real) for p in points)
            ys = max(int(p.imag) for p in points)
            print(xs, ys)
        for y in range(ys+1):
            row = ''
            for x in range(xs+1):
                if (x + y * 1j) in points:
                    row += "#"
                else:
                    row += " "
            print(row)
                    

        


    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        dots, instructions = puzzle_input.split("\n\n")
        points = set()
        for line in dots.splitlines():
            x, y = line.split(",")
            points.add(int(x) + int(y) * 1j)
        instructions2 = []
        for line in instructions.splitlines():
            _, _, instruction = line.split()
            a, b = instruction.split("=")
            instructions2.append((a, int(b)))
        return points, instructions2


if __name__ == "__main__":
    typer.run(Day13().run)

# vim:expandtab:sw=4:ts=4
