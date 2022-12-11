#!/bin/python
"""Advent of Code, Day 18: Like a GIF For Your Yard. Conway's Game of Life."""

import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = """\
.#.#.#
...##.
#....#
..#...
#.#..#
####.."""

LineType = int
InputType = list[LineType]


class Day18(aoc.Challenge):
    """Day 18: Like a GIF For Your Yard."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=4),
        aoc.TestCase(inputs=SAMPLE, part=2, want=17),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_one_str

    def part1(self, parsed_input: InputType) -> int:
        b = aoc.Board.from_block_map(parsed_input, lambda x: x == "#")
        cycles = 4 if self.testing else 100
        for step in range(cycles):
            print(step, sum(b.values()))
            new = aoc.Board()
            for point, on in b.items():
                if on:
                    new[point] = sum(b[p] for p in b.neighbors(point, True)) in (2, 3)
                else:
                    new[point] = sum(b[p] for p in b.neighbors(point, True)) == 3
            b = new
        return sum(b.values())

    def part2(self, parsed_input: InputType) -> int:
        b = aoc.Board.from_block_map(parsed_input, lambda x: x == "#")
        cycles = 5 if self.testing else 100
        for step in range(cycles):
            for i in (0, complex(0, b.height - 1), complex(b.width - 1, 0), complex(b.width - 1, b.height - 1)):
                b[i] = True
            print(step, sum(b.values()))
            new = aoc.Board()
            for point, on in b.items():
                if on:
                    new[point] = sum(b[p] for p in b.neighbors(point, True)) in (2, 3)
                else:
                    new[point] = sum(b[p] for p in b.neighbors(point, True)) == 3
            b = new
        for i in (0, complex(0, b.height - 1), complex(b.width - 1, 0), complex(b.width - 1, b.height - 1)):
            b[i] = True
        return sum(b.values())



    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().input_parser(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]
        # Words: mixed str and int
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in line.split()
            )
            for line in puzzle_input.splitlines()
        ]
        # Regex splitting
        patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in patt.match(line).groups()
            )
            for line in puzzle_input.splitlines()
        ]

    # def line_parser(self, line: str):
    #     pass


if __name__ == "__main__":
    typer.run(Day18().run)

# vim:expandtab:sw=4:ts=4
