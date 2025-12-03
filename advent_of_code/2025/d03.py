#!/bin/python
"""Advent of Code, Day 3: Lobby."""

from lib import aoc

SAMPLE = """\
987654321111111
811111111111119
234234234234278
818181911112111"""


class Day03(aoc.Challenge):
    """Day 3: Lobby."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=357),
        aoc.TestCase(part=2, inputs=SAMPLE, want=3121910778619),
    ]
    INPUT_PARSER = aoc.parse_one_str_per_line

    def solver(self, puzzle_input: list[str], part_one: bool) -> int:
        total = 0
        size = 2 if part_one else 12
        for line in puzzle_input:
            digits = []
            for save in range(size)[::-1]:
                biggest = max(line[:-save] if save else line)
                digits.append(biggest)
                line = line[line.index(biggest) + 1:]

            total += int("".join(digits))
        return total

# vim:expandtab:sw=4:ts=4
