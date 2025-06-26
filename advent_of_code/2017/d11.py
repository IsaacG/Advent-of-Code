#!/bin/python
"""Advent of Code, Day 11: Hex Ed."""

from lib import aoc

SAMPLE = [
    ('ne,ne,ne', 3),
    ('ne,ne,sw,sw', 0),
    ('ne,ne,s,s', 2),
    ('se,sw,se,sw,sw', 3),
]
OFFSETS = aoc.HEX_AXIAL_DIRS_FLAT_TOP


class Day11(aoc.Challenge):
    """Day 11: Hex Ed."""

    TESTS = [
        aoc.TestCase(part=1, inputs=data, want=want)
        for data, want in SAMPLE
    ] + [
        aoc.TestCase(part=2, inputs="", want=aoc.TEST_SKIP),
    ]

    def solver(self, puzzle_input: str, part_one: bool) -> int:
        """Walk a hex grid and compute distances."""
        location = complex(0, 0)
        farthest = 0

        def axial_distance() -> int:
            """Taken from https://www.redblobgames.com/grids/hexagons/#distances."""
            q, r = int(location.real), int(location.imag)
            return (abs(q) + abs(q + r) + abs(r)) // 2

        for direction in puzzle_input.split(","):
            location += OFFSETS[direction]
            farthest = max(farthest, axial_distance())
        return axial_distance() if part_one else farthest
