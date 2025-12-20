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


def is_real(name: str, checksum: str) -> bool:
    """Return if a name matches its checksum."""
    name = name.replace("-", "")
    top = sorted((-v, k) for k, v in collections.Counter(name).items())
    return "".join(b for a, b in top[:5]) == checksum


def solve(data: InputType, part: int) -> int:
    """Return the sector with Northpole storage."""
    real_sectors = (
        (name, sector, checksum) for name, sector, checksum in data
        if is_real(name, checksum)
    )
    if part == 1:
        # Return the sum of real sectors.
        return sum(sector for name, sector, checksum in real_sectors)
    for name, sector, checksum in real_sectors:
        name = "".join(
            string.ascii_lowercase[
                (string.ascii_lowercase.index(i) + sector) % 26
            ] if i.isalpha() else " "
            for i in name
        )
        if "northpole" in name.split():
            return sector
    raise RuntimeError("No solution found.")


PARSER = aoc.parse_re_group_mixed(r"([\w-]+)-(\d+)\[(\w+)\]")
TESTS = [(1, SAMPLE, 1514)]
