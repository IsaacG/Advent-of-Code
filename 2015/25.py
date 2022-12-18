#!/bin/python
"""Advent of Code, Day 25: Let It Snow. Compute the code needed to start the machine."""

import typer
from lib import aoc

SAMPLE = ["1 1", "2 6", "6 4"]

LineType = list[int]
InputType = list[LineType]


class Day25(aoc.Challenge):
    """Day 25: Let It Snow."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=20151125),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=4041754),
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=24659492),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_re_findall_int(r"\d+")

    def part1(self, parsed_input: InputType) -> int:
        """Return the code given on a row/column."""
        row, column = parsed_input[0]
        # Determine the code generation number based on row/column.
        code_num = 1
        for i in range(1, row):
            code_num += i
        for i in range(row + 1, row + column):
            code_num += i
        # Starting code, given in the puzzle.
        code = 20151125
        # Generate new codes n times until we get the one we need.
        for i in range(code_num - 1):
            code = (code * 252533) % 33554393
        return code

    def part2(self, parsed_input: InputType) -> int:
        return 0


if __name__ == "__main__":
    typer.run(Day25().run)

# vim:expandtab:sw=4:ts=4
