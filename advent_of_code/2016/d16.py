#!/bin/python
"""Advent of Code, Day 16: Dragon Checksum.

Compute a repeat-checksum of dragon-curve data.
"""

import collections
from collections.abc import Generator
import more_itertools


def solve(data: list[bool], part: int, testing: bool) -> str:
    """Generate a dragon checksum."""
    length = 20 if testing else 272 if part == 1 else 35651584

    # Compute the size of the output.
    # length / size gives the number of bits per output checksum bit.
    size = length
    while size % 2 == 0:
        size //= 2

    def separator_gen() -> Generator[bool, None, None]:
        """Generate the separate bits."""
        generated: list[bool] = []
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

    def checksum_gen(disk_data: Generator[bool, None, None]) -> Generator[bool, None, None]:
        """Generate the checksum bits from the random disk bits.

        This can also be approached rescursively (see commit 57c55df) but that performed slower.
        """
        checksum_width = length // size
        queue: collections.deque[bool] = collections.deque()

        while True:
            queue.extend(next(disk_data) == next(disk_data) for _ in range(checksum_width // 2))
            while len(queue) > 1:
                queue.append(queue.popleft() == queue.popleft())
            yield queue.pop()

    out_stream = checksum_gen(bit_gen(data, separator_gen()))
    return "".join("1" if i else "0" for i in more_itertools.take(size, out_stream))


def input_parser(data: str) -> list[bool]:
    """Parse the input data."""
    return [i == "1" for i in data]


TESTS = [(1, "10000", "01100")]
