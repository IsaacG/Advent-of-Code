#!/bin/python
"""Advent of Code, Day 11: Chronal Charge."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = ["18", "42"]
LineType = int
InputType = list[LineType]


class Day11(aoc.Challenge):
    """Day 11: Chronal Charge."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want="33,45"),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want="21,61"),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want="90,269,16"),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want="232,251,12"),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_one_int

    def part1(self, parsed_input: InputType) -> int:
        serial = parsed_input
        
        def power_level(x: int, y: int) -> int:
            rack_id = x + 10
            power = rack_id * (rack_id * y + serial)
            return ((power // 100) % 10) - 5

        grid = []
        for y in range(300):
            row = []
            for x in range(300):
                row.append(power_level(x + 1, y + 1))
            grid.append(row)

        xgroups = []
        for row in grid:
            xrow = []
            window = row[0] + row[1]
            for x in range(298):
                window += row[x + 2]
                xrow.append(window)
                window -= row[x]
            xgroups.append(xrow)

        ygroups = []
        for col in zip(*xgroups):
            ycol = []
            window = col[0] + col[1]
            for y in range(298):
                window += col[y + 2]
                ycol.append(window)
                window -= col[y]
            ygroups.append(ycol)

        groups = list(zip(*ygroups))
        val, x, y = max(
            (val, x, y)
            for y, row in enumerate(groups)
            for x, val in enumerate(row)
        )
        return f"{x + 1},{y + 1}"

    def part2(self, parsed_input: InputType) -> int:
        serial = parsed_input
        
        def power_level(x: int, y: int) -> int:
            rack_id = x + 10
            power = rack_id * (rack_id * y + serial)
            return ((power // 100) % 10) - 5

        grid = []
        for y in range(300):
            row = []
            for x in range(300):
                row.append(power_level(x + 1, y + 1))
            grid.append(row)

        def max_grid(size: int) -> tuple[int, int]:
            xgroups = []
            for row in grid:
                xrow = []
                window = sum(row[:size])
                for x in range(300 - size):
                    window += row[x + size]
                    xrow.append(window)
                    window -= row[x]
                xgroups.append(xrow)

            ygroups = []
            for col in zip(*xgroups):
                ycol = []
                window = sum(col[:size])
                for y in range(300 - size):
                    window += col[y + size]
                    ycol.append(window)
                    window -= col[y]
                ygroups.append(ycol)

            groups = list(zip(*ygroups))
            return max(
                (val, x, y)
                for y, row in enumerate(groups)
                for x, val in enumerate(row)
            )

        (val, x, y), size = max(
            (max_grid(size), size)
            for size in range(300)
        )

        return f"{x + 1},{y + 1},{size + 1}"


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


if __name__ == "__main__":
    typer.run(Day11().run)

# vim:expandtab:sw=4:ts=4
