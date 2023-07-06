#!/bin/python
"""Advent of Code, Day 4: Security Through Obscurity."""
from __future__ import annotations

import collections
import string

from lib import aoc

SAMPLE = """\
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]"""

InputType = list[tuple[str, int, str]]


class Day04(aoc.Challenge):
    """Day 4: Security Through Obscurity."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=1514),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_re_group_mixed(r"([\w-]+)-(\d+)\[(\w+)\]")

    def is_real(self, name: str, checksum: str) -> bool:
        """Return if a name matches its checksum."""
        name = name.replace("-", "")
        top = sorted((-v, k) for k, v in collections.Counter(name).items())
        return "".join(b for a, b in top[:5]) == checksum

    def part1(self, parsed_input: InputType) -> int:
        """Return the sum of real sectors."""
        return sum(
            sector
            for name, sector, checksum in parsed_input
            if self.is_real(name, checksum)
        )

    def part2(self, parsed_input: InputType) -> int:
        """Return the sector with Northpole storage."""
        for name, sector, checksum in parsed_input:
            if not self.is_real(name, checksum):
                continue
            name = "".join(
                string.ascii_lowercase[
                    (string.ascii_lowercase.index(i) + sector) % 26
                ] if i.isalpha() else " "
                for i in name
            )
            if "northpole" in name.split():
                return sector
        raise RuntimeError("No solution found.")
