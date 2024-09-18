#!/bin/python
"""Advent of Code, Day 10: Knot Hash."""
import functools
import math

import more_itertools
from lib import aoc


def tie_knots(lengths: list[int], size: int) -> list[int]:
    """Return list with knots tied at each length."""
    data = list(range(size))
    position = 0
    for skip, length in enumerate(lengths):
        # Reverse the length-span.
        data = list(reversed(data[:length])) + data[length:]
        # "Shift left" so the list starts at the position pointer.
        split = (length + skip) % size
        data = data[split:] + data[:split]
        position += length + skip

    # Shift the list based on the position so the position is actually
    # offset and not at "0".
    split = size - (position % size)
    return data[split:] + data[:split]


def knot_hash(data: list[int]) -> str:
        data = tie_knots(data * 64, 256)
        # Chunk and XOR in chunks of 16.
        dense = [
            functools.reduce(lambda a, b: a ^ b, chunk)
            for chunk in more_itertools.chunked(data, 16)
        ]
        # Format as two-char hex values.
        return "".join(f"{i:02x}" for i in dense)


class Day10(aoc.Challenge):
    """Day 10: Knot Hash."""

    TESTS = [
        aoc.TestCase(part=1, inputs="0", want=0),
        aoc.TestCase(part=1, inputs="4", want=6),
        aoc.TestCase(part=1, inputs="3,4,1,5", want=12),
        aoc.TestCase(part=2, inputs="", want="a2582a3a0e66e6e86e3812dcb672a272"),
        aoc.TestCase(part=2, inputs="AoC 2017", want="33efeb34ea91902bb2f59c9920caa6cd"),
        aoc.TestCase(part=2, inputs="1,2,3", want="3efbe78a8d82f29979031a4aa0b16a9d"),
        aoc.TestCase(part=2, inputs="1,2,4", want="63960835bcdc130f0b66d7ff4f6a5a8e"),
    ]
    INPUT_PARSER = aoc.parse_one_str

    def part1(self, puzzle_input: str) -> int:
        """Tie knots and return the product of the first two values."""
        # Parse the input as a list of numbers.
        lengths = [int(i) for i in puzzle_input.split(",")]
        size = 5 if self.testing else 256
        data = tie_knots(lengths, size)
        return math.prod(data[:2])

    def part2(self, puzzle_input: str) -> str:
        """Tie knots 64 times then densify and hexify."""
        # Parse the input as a list of ASCII bytes.
        lengths = [ord(i) for i in puzzle_input] + [17, 31, 73, 47, 23]
        return knot_hash(lengths)
