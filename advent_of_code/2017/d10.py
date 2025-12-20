#!/bin/python
"""Advent of Code, Day 10: Knot Hash."""
import functools
import math

import more_itertools


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
    """Return the hash of data."""
    data = tie_knots(data * 64, 256)
    # Chunk and XOR in chunks of 16.
    dense = [
        functools.reduce(lambda a, b: a ^ b, chunk)
        for chunk in more_itertools.chunked(data, 16)
    ]
    # Format as two-char hex values.
    return "".join(f"{i:02x}" for i in dense)


def solve(data: str, part: int, testing: bool) -> int | str:
    """Tie knots."""
    if part == 1:
        # Parse the input as a list of numbers.
        lengths = [int(i) for i in data.split(",")]
        size = 5 if testing else 256
        knots = tie_knots(lengths, size)
        return math.prod(knots[:2])

    # Tie knots 64 times then densify and hexify.
    # Parse the input as a list of ASCII bytes.
    lengths = [ord(i) for i in data] + [17, 31, 73, 47, 23]
    return knot_hash(lengths)


PARSER = str
TESTS = [
    (1, "0", 0),
    (1, "4", 6),
    (1, "3,4,1,5", 12),
    (2, "", "a2582a3a0e66e6e86e3812dcb672a272"),
    (2, "AoC 2017", "33efeb34ea91902bb2f59c9920caa6cd"),
    (2, "1,2,3", "3efbe78a8d82f29979031a4aa0b16a9d"),
    (2, "1,2,4", "63960835bcdc130f0b66d7ff4f6a5a8e"),
]
