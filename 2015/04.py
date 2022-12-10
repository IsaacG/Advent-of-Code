#!/bin/python
"""Advent of Code: Day 04."""

import hashlib

import typer
from lib import aoc

SAMPLE = ["abcdef", "pqrstuv"]
InputType = list[int]


class Day04(aoc.Challenge):
    """Day 4: The Ideal Stocking Stuffer. MD5 mine for a good hash."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=609043),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=1048970),
    )
    INPUT_PARSER = aoc.parse_one_str

    def generic(self, key: InputType, size: int) -> int:
        """Return a suffix which generates a hash starting with a given prefix."""
        prefix = "0" * size
        md5 = hashlib.md5(key.encode())
        for i in range(0, 100000000):
            md5copy = md5.copy()
            md5copy.update(str(i).encode())
            if md5copy.hexdigest().startswith(prefix):
                return i
        raise RuntimeError("Not found")

    def part1(self, parsed_input: InputType) -> int:
        """Return a suffix which generates a 5-zeroes hash."""
        return self.generic(parsed_input, 5)

    def part2(self, parsed_input: InputType) -> int:
        """Return a suffix which generates a 6-zeroes hash."""
        return self.generic(parsed_input, 6)


if __name__ == "__main__":
    typer.run(Day04().run)

# vim:expandtab:sw=4:ts=4
