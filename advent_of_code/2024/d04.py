#!/bin/python
"""Advent of Code, Day 4: Ceres Search."""

from lib import aoc

SAMPLE = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""


class Day04(aoc.Challenge):
    """Day 4: Ceres Search. Word search."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=18),
        aoc.TestCase(part=2, inputs=SAMPLE, want=9),
    ]
    INPUT_PARSER = aoc.CoordinatesParserC()

    def part1(self, puzzle_input: aoc.Map) -> int:
        """Count occurances of XMAS in the word search."""
        return sum(
            all(
                (start + distance * direction) in puzzle_input.coords[letter]
                for distance, letter in enumerate("MAS", start=1)
            )
            for start in puzzle_input.coords["X"]
            for direction in aoc.EIGHT_DIRECTIONS
        )

    def part2(self, puzzle_input: aoc.Map) -> int:
        """Count occurances of MAS in an X shape in the word search."""
        want = {
            complex(-1, -1): "M",
            complex(-1, 1): "M",
            complex(1, 1): "S",
            complex(1, -1): "S",
        }
        return sum(
            all(
                (start + offset * 1j ** rotation) in puzzle_input.coords[letter]
                for offset, letter in want.items()
            )
            for start in puzzle_input.coords["A"]
            for rotation in range(4)
        )

# vim:expandtab:sw=4:ts=4
