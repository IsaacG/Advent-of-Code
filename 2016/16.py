#!/bin/python
"""Advent of Code, Day 16: Dragon Checksum. Compute a repeat-checksum of dragon-curve data."""

import collections
import math
from collections.abc import Generator
import more_itertools
from lib import aoc

InputType = list[bool]


class Day16(aoc.Challenge):
    """Day 16: Dragon Checksum."""

    TESTS = [
        aoc.TestCase(inputs="10000", part=1, want="01100"),
        aoc.TestCase(inputs="", part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> str:
        length = 20 if self.testing else 272
        data = parsed_input

        # Expand with the Dragon Curve.
        while len(data) < length:
            data = data + [False] + [not i for i in reversed(data)]
        data = data[:length]
        # Checksum the bits.
        while len(data) % 2 == 0:
            data = [a == b for a, b in more_itertools.chunked(data, 2)]
        return "".join("1" if i else "0" for i in data)

    def part2(self, parsed_input: InputType) -> int:
        length = 35651584

        # Compute the size of the output.
        # length / size gives the number of bits per output checksum bit.
        size = length
        while size % 2 == 0:
            size //= 2

        def separator_gen() -> Generator[bool, None, None]:
            """Generate the separate bits."""
            generated = []
            while True:
                add = [False] + [not i for i in reversed(generated)]
                yield from add
                generated.extend(add)

        def bit_gen(data: list[bool], separator: Generator[bool, None, None]) -> Generator[bool, None, None]:
            """Generate the post-curve disk data bits.

            This data is the original disk data, forward then backwards, with separator bits in between.
            """
            reversed_data = [not i for i in reversed(data)]
            while True:
                yield from data
                yield next(separator)
                yield from reversed_data
                yield next(separator)

        disk_data = bit_gen(parsed_input, separator_gen())
        checksum_width = length // size
        checksum_levels = math.log2(checksum_width)

        def checksum_gen(depth: int) -> bool:
            """Generate the checksum bits from the random disk bits."""
            if depth:
                return checksum_gen(depth - 1) == checksum_gen(depth - 1)
            return next(disk_data)

        checksum_bits = (checksum_gen(checksum_levels) for _ in range(size))
        return "".join("1" if i else "0" for i in checksum_bits)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [i == "1" for i in puzzle_input]
