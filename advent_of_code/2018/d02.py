#!/bin/python
"""Day 2: Inventory Management System.

Find the storage boxes with Santa's cloth.
Count char occurances to checksum IDs then find IDs with hamming distance 1.
"""

import collections
import itertools
from typing import Dict, List

from lib import aoc

SAMPLE = ["""\
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz"""]


def hamming_distance(a, b):
    return sum(i != j for i, j in zip(a, b))


class Day02(aoc.Challenge):

    TESTS = (aoc.TestCase(inputs=SAMPLE[0], part=2, want='fgij'),)
    INPUT_PARSER = aoc.parse_one_str_per_line

    def part1(self, puzzle_input: List[str]) -> int:
        """Return the number of IDs that contain exactly 2|3 repeat letters."""
        # Also, functools.reduce()
        total: Dict[int, int] = collections.Counter([])
        for line in puzzle_input:
            c = collections.Counter(line)
            total += collections.Counter(set(c.values()))
        return total[2] * total[3]

    def part2(self, puzzle_input: List[str]) -> str:
        """Return the common chars in two IDs with hamming distance 1."""
        for a, b in itertools.combinations(puzzle_input, 2):
            if hamming_distance(a, b) == 1:
                return "".join(i for i, j in zip(a, b) if i == j)
        raise RuntimeError
