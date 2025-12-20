#!/bin/python
"""Advent of Code, Day 11: Hex Ed."""

from lib import aoc
OFFSETS = aoc.HEX_AXIAL_DIRS_FLAT_TOP


def solve(data: str, part: int) -> int:
    """Walk a hex grid and compute distances."""
    location = complex(0, 0)
    farthest = 0

    def axial_distance() -> int:
        """Taken from https://www.redblobgames.com/grids/hexagons/#distances."""
        q, r = int(location.real), int(location.imag)
        return (abs(q) + abs(q + r) + abs(r)) // 2

    for direction in data.split(","):
        location += OFFSETS[direction]
        farthest = max(farthest, axial_distance())
    return axial_distance() if part == 1 else farthest


TESTS = [
    (1, 'ne,ne,ne', 3),
    (1, 'ne,ne,sw,sw', 0),
    (1, 'ne,ne,s,s', 2),
    (1, 'se,sw,se,sw,sw', 3),
]
