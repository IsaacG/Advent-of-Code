#!/bin/python
"""Day 2: Inventory Management System.

Find the storage boxes with Santa's cloth.
Count char occurances to checksum IDs then find IDs with hamming distance 1.
"""
import collections
import itertools
from lib import aoc


def solve(data: list[str], part: int) -> int:
    """Return the number of IDs that contain exactly 2|3 repeat letters."""
    if part == 1:
        total: dict[int, int] = collections.Counter([])
        for line in data:
            c = collections.Counter(line)
            total += collections.Counter(set(c.values()))
        return total[2] * total[3]

    """Return the common chars in two IDs with hamming distance 1."""
    for a, b in itertools.combinations(data, 2):
        if sum(i != j for i, j in zip(a, b)) == 1:
            return "".join(i for i, j in zip(a, b) if i == j)
    raise RuntimeError


PARSER = str.splitlines
SAMPLE = ["""\
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz"""]
TESTS = [(2, SAMPLE[0], 'fgij')]
