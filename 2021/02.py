#!/bin/python

"""Advent of Code: Day 02."""

import typer

from lib import aoc


SAMPLE = ["""\
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""]


class Day02(aoc.Challenge):
    """Track the location of the submarine as it moves about."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=150),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=900),
    )
    INPUT_TYPES = [str, int]

    def part1(self, lines: list[tuple[str, int]]) -> int:
        """Compute the submarine's horizontal position and depth."""
        horiz, depth = 0, 0
        for direction, num in lines:
            if direction == "forward":
                horiz += num
            if direction == "up":
                depth -= num
            if direction == "down":
                depth += num

        return depth * horiz

    def part2(self, lines: list[tuple[str, int]]) -> int:
        """Compute the submarine's horizontal position, depth and aim."""
        horiz, depth, aim = 0, 0, 0
        for direction, num in lines:
            if direction == "forward":
                horiz += num
                depth += aim * num
            if direction == "up":
                aim -= num
            if direction == "down":
                aim += num

        return horiz * depth


if __name__ == '__main__':
    typer.run(Day02().run)
