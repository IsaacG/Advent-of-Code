#!/bin/python
"""Advent of Code, Day 4: The Ideal Stocking Stuffer. MD5 mine for a good hash."""

import hashlib
import itertools


def solve(data: str, part: int) -> int:
    """Return a suffix which generates a hash starting with a given prefix."""
    size = 5 if part == 1 else 6
    prefix = "0" * size
    md5 = hashlib.md5(data.encode())
    for i in itertools.count():
        md5copy = md5.copy()
        md5copy.update(str(i).encode())
        if md5copy.hexdigest().startswith(prefix):
            return i
    raise RuntimeError("Not found")


TESTS = [
    (1, "abcdef", 609043),
    (1, "pqrstuv", 1048970),
]
