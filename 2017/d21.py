#!/bin/python
"""Advent of Code, Day 21: Fractal Art."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#""",  # 16
]
STARTING_PATTERN = """\
.#.
..#
###"""
START = {
    complex(x, y)
    for y, line in enumerate(STARTING_PATTERN.splitlines())
    for x, char in enumerate(line)
    if char == "#"
}
SHIFT = complex(1, 1)

LineType = int
InputType = list[LineType]


def to_complex_set(pattern: str) -> set[complex]:
    return {
        complex(x, y)
        for y, part in enumerate(pattern.split("/"))
        for x, char in enumerate(part)
        if char == "#"
    }


def permutations(pixels: frozenset[complex], block_size: int) -> list[frozenset[complex]]:
    hashes = set(pixels)

    # Shift the pattern to center around (0, 0) to make flip/rotate simpler.
    if block_size == 2:
        hashes = {i * 2 for i in hashes}
    hashes = {i - SHIFT for i in hashes}
    flipped = {complex(-i.real, +i.imag) for i in hashes}
    # Rotate and flip.
    matches = [
        {i * 1j ** rot for i in j} for rot in range(4)
        for j in [hashes, flipped]
    ]
    # Unshift.
    matches = [
        {i + SHIFT for i in hashes}
        for hashes in matches
    ]
    if block_size == 2:
        matches = [{i / 2 for i in hashes} for hashes in matches]
    return {frozenset(i) for i in matches}

def pprint(pixels, size) -> None:
    for y in range(size):
        line = ""
        for x in range(size):
            line += "#" if complex(x, y) in pixels else "."
        # print(line)


class Day21(aoc.Challenge):
    """Day 21: Fractal Art."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    PARAMETERIZED_INPUTS = [5, 18]

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=12),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    def solver(self, parsed_input: InputType, param: int) -> int | str:
        pixels = START
        replacements = parsed_input
        size = 3
        step = 0
        subpixels = {i: {complex(x, y) for x in range(i) for y in range(i)} for i in [2, 3]}

        for step in range(2 if self.testing else param):
            blocksize_in = 3 if size % 2 else 2
            blockcount = size // blocksize_in
            blocksize_out = blocksize_in + 1

            size += blockcount

            new_pixels = set()
            for y in range(blockcount):
                for x in range(blockcount):
                    corner_in = complex(x * blocksize_in, y * blocksize_in)
                    corner_out = complex(x * blocksize_out, y * blocksize_out)
                    subpixels_in = frozenset({p for p in subpixels[blocksize_in] if corner_in + p in pixels})
                    # print(corner_in)
                    # pprint(subpixels_in, blocksize_in)
                    subpixels_out = {corner_out + p for p in replacements[blocksize_in][subpixels_in]}
                    new_pixels.update(subpixels_out)

            # print(f"{step + 1}: {len(pixels)} => {len(new_pixels)} pixels on")
            pixels = new_pixels
            # print("Step ", step + 1)
            # pprint(pixels, size)
            # print()

        # print(f"{step}: {size}x{size} = {len(pixels)} pixels on")
        if False:
            print(f"{step}: {size}x{size} = {len(pixels)}")
            print()
            pprint(pixels, size)
            print()

        got = len(pixels)
        if not self.testing:
            # assert 199 < got < 224, got
            pass
        return got

        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""

        # Parse the inputs into rules.
        rules = {2: {}, 3: {}}
        for line in puzzle_input.splitlines():
            match, _, replace = line.split()
            block_size = 2 if len(match) == 5 else 3
            rules[block_size][frozenset(to_complex_set(match))] = to_complex_set(replace)

        # Build the enhance dict.
        return {
            block_size: {
                match: replace
                for match, replace in block_rules.items()
                for match in permutations(match, block_size)
            }
            for block_size, block_rules in rules.items()
        }


# vim:expandtab:sw=4:ts=4
