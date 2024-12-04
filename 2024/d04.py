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
    INPUT_PARSER = aoc.char_map

    def part1(self, puzzle_input: dict[complex, str]) -> int:
        """Count occurances of XMAS in the word search."""
        return sum(
            all(
                puzzle_input.get(start + distance * direction) == letter
                for distance, letter in enumerate("XMAS")
            )
            for start in puzzle_input
            for direction in aoc.EIGHT_DIRECTIONS
        )

    def part2(self, puzzle_input: dict[complex, str]) -> int:
        """Count occurances of MAS in an X shape in the word search."""
        want = {
            complex(0, 0): "M",
            complex(0, 2): "M",
            complex(1, 1): "A",
            complex(2, 2): "S",
            complex(2, 0): "S",
        }
        return sum(
            all(
                puzzle_input.get(start + offset * 1j ** rotation) == letter
                for offset, letter in want.items()
            )
            for start in puzzle_input
            for rotation in range(4)
        )

# vim:expandtab:sw=4:ts=4
