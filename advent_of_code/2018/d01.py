#!/bin/python
"""Day 1: Chronal Calibration.

Sum up frequencies then do so repeatedly until a repeat is seen.
"""

import itertools
from typing import List

from lib import aoc


class Day01(aoc.Challenge):

    def part1(self, puzzle_input: List[int]) -> int:
        return sum(puzzle_input)

    def part2(self, puzzle_input: List[int]) -> int:
        seen = set()
        freq = 0
        it = itertools.cycle(puzzle_input)
        while freq not in seen:
            seen.add(freq)
            freq += next(it)
        return freq
