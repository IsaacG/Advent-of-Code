#!/bin/python
"""Advent of Code, Day 3: Gear Ratios."""

import math
import re

from lib import aoc

SAMPLE = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

InputType = None


class Day03(aoc.Challenge):
    """Day 3: Gear Ratios."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=4361),
        aoc.TestCase(inputs=SAMPLE, part=2, want=467835),
    ]

    def part1(self, parsed_input: InputType) -> int:
        """Sum up all engine part numbers."""
        number_by_start, coord_to_number, engine_parts = parsed_input
        # Map engine parts to neighboring positions to unique part numbers.
        all_nums = {
            coord_to_number[neighbor]
            for pos in engine_parts
            for neighbor in aoc.neighbors(pos, directions=aoc.EIGHT_DIRECTIONS)
            if neighbor in coord_to_number
        }
        return sum(number_by_start[pos] for pos in all_nums)

    def part2(self, parsed_input: InputType) -> int:
        """Sum up all gear ratios."""
        number_by_start, coord_to_number, engine_parts = parsed_input
        # Find gear parts and map them to neighboring numbers.
        ratios = (
            {
                coord_to_number[neighbor]
                for neighbor in aoc.neighbors(pos, directions=aoc.EIGHT_DIRECTIONS)
                if neighbor in coord_to_number
            }
            for pos, char in engine_parts.items()
            if char == "*"
        )
        # Sum up the product of ratios when exactly two exist for a given gear.
        return sum(
            math.prod(number_by_start[pos] for pos in nums)
            for nums in ratios
            if len(nums) == 2
        )

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        # Part numbers by the coordinate of the first digit.
        number_by_start: dict[complex, int] = {}
        # Map all digits to the location of the first digit in the number.
        coord_to_number: dict[complex, complex] = {}
        # Map all engine parts, location to symbol.
        engine_parts: dict[complex, str] = {}

        for y_pos, line in enumerate(puzzle_input.splitlines()):
            for match in re.finditer(r"\d+", line):
                start, end = match.span()
                val = int(match.group())
                number_by_start[complex(start, y_pos)] = val
                for x_pos in range(start, end):
                    coord_to_number[complex(x_pos, y_pos)] = complex(start, y_pos)
            for x_pos, char in enumerate(line):
                if not char.isdigit() and char != ".":
                    engine_parts[complex(x_pos, y_pos)] = char
        return number_by_start, coord_to_number, engine_parts

# vim:expandtab:sw=4:ts=4
