#!/bin/python
"""Advent of Code: Day 04."""

import hashlib

from lib import aoc

SAMPLE = ["abcdef", "pqrstuv"]


class Day04(aoc.Challenge):
    """Day 4: The Ideal Stocking Stuffer. MD5 mine for a good hash."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=609043),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=1048970),
    ]

    def solver(self, key: list[int], part_one: bool) -> int:
        """Return a suffix which generates a hash starting with a given prefix."""
        size = 5 if part_one else 6
        prefix = "0" * size
        md5 = hashlib.md5(key.encode())
        for i in range(0, 100000000):
            md5copy = md5.copy()
            md5copy.update(str(i).encode())
            if md5copy.hexdigest().startswith(prefix):
                return i
        raise RuntimeError("Not found")
