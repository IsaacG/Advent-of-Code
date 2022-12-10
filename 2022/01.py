#!/bin/python
"""Advent of Code: Day 01."""

import typer
from lib import aoc

SAMPLE = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""
InputType = list[list[int]]


class Day01(aoc.Challenge):
    """Day 1: Calorie Counting. Count how many calories the elves have."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=24000),
        aoc.TestCase(inputs=SAMPLE, part=2, want=45000),
    ]
    INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_int_per_line])

    def part1(self, parsed_input: InputType) -> int:
        """Return the sum calories held by the elf with the most calories."""
        return max(sum(i) for i in parsed_input)

    def part2(self, parsed_input: InputType, top_n: int = 3) -> int:
        """Return the sum calories held by the top three elves with the most calories."""
        return sum(sorted(sum(i) for i in parsed_input)[-top_n:])

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [
            [int(line) for line in block.splitlines()]
            for block in puzzle_input.split("\n\n")
        ]


if __name__ == "__main__":
    typer.run(Day01().run)

# vim:expandtab:sw=4:ts=4
