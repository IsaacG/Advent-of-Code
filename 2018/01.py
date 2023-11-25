#!/bin/python
"""Day 1: Chronal Calibration.

Sum up frequencies then do so repeatedly until a repeat is seen.
"""

import itertools
from typing import List

from lib import aoc


class Day01(aoc.Challenge):

    def part1(self, parsed_input: List[int]) -> int:
        return sum(parsed_input)

    def part2(self, parsed_input: List[int]) -> int:
        seen = set()
        freq = 0
        it = itertools.cycle(parsed_input)
        while freq not in seen:
            seen.add(freq)
            freq += next(it)
        return freq

    def input_parser(self, puzzle_input: str) -> List[int]:
        return [int(i) for i in puzzle_input.split('\n')]
