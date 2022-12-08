#!/bin/python
"""Advent of Code, Day 14: Reindeer Olympics."""

import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = ["""\
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."""
]

LineType = int
InputType = list[LineType]


class Day14(aoc.Challenge):
    """Day 14: Reindeer Olympics."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=1120),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=689),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    # Convert lines to type:
    INPUT_TYPES = LineType
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        seconds = 1000 if self.testing else 2503

        distances = []
        for _, speed, fly, rest in parsed_input:
            rounds, extra = divmod(seconds, fly + rest)
            distance = speed * (rounds * fly + min(extra, fly))
            distances.append(distance)
        return max(distances)

    def part2(self, parsed_input: InputType) -> int:
        race_len = 1000 if self.testing else 2503

        points = {name: 0 for name, *_ in parsed_input}

        def distance(seconds, speed, fly, rest):
            rounds, extra = divmod(seconds, fly + rest)
            return speed * (rounds * fly + min(extra, fly))

        for i in range(1, race_len + 1):
            positions = {
                    name: distance(i, speed, fly, rest)
                for name, speed, fly, rest in parsed_input
            }
            max_position = max(positions.values())
            for name, position in positions.items():
                if position == max_position:
                    points[name] += 1
        print(points)
        return max(points.values())

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().input_parser(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]

    def line_parser(self, line: str) -> LineType:
        """If defined, use this to parse single lines."""
        patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
        return tuple(
            int(i) if i.isdigit() else i
            for i in patt.match(line).groups()
        )


if __name__ == "__main__":
    typer.run(Day14().run)

# vim:expandtab:sw=4:ts=4
