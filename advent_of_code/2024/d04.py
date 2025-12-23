#!/bin/python
"""Advent of Code, Day 4: Ceres Search. Word search."""
from lib import aoc
PARSER = aoc.CoordinatesParserC()


def solve(data: aoc.Map, part: int) -> int:
    """Count occurances of XMAS in the word search."""
    if part == 1:
        return sum(
            all(
                (start + distance * direction) in data.coords[letter]
                for distance, letter in enumerate("MAS", start=1)
            )
            for start in data.coords["X"]
            for direction in aoc.EIGHT_DIRECTIONS
        )

    # Look for an X shape.
    want = {
        complex(-1, -1): "M",
        complex(-1, 1): "M",
        complex(1, 1): "S",
        complex(1, -1): "S",
    }
    return sum(
        all(
            (start + offset * 1j ** rotation) in data.coords[letter]
            for offset, letter in want.items()
        )
        for start in data.coords["A"]
        for rotation in range(4)
    )


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
TESTS = [(1, SAMPLE, 18), (2, SAMPLE, 9)]
# vim:expandtab:sw=4:ts=4
