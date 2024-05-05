#!/bin/python
"""Day 1: Chronal Calibration.

Compute overlapping rectangles which the elves want to cut from fabric.
"""

import re
from typing import List, Set, Tuple

from lib import aoc


class Day03(aoc.Challenge):

    def get_overlap(self, parsed_input: List[List[int]]) -> Set[Tuple[int, int]]:
        """Calculate the overlapping squares."""
        seen_once = set()
        seen_twice = set()
        for i, x, y, w, h in parsed_input:
            for a in range(x, x + w):
                for b in range(y, y + h):
                    if (a, b) in seen_once:
                        seen_twice.add((a, b))
                    else:
                        seen_once.add((a, b))
        return seen_twice

    def part1(self, parsed_input: List[List[int]]) -> int:
        return len(self.get_overlap(parsed_input))

    def part2(self, parsed_input: List[List[int]]) -> int:
        """Find the pattern which has no overlap with any others."""
        seen_twice = self.get_overlap(parsed_input)

        for i, x, y, w, h in parsed_input:
            if all((a, b) not in seen_twice for a in range(x, x + w) for b in range(y, y + h)):
                return i
        raise RuntimeError

    def input_parser(self, puzzle_input: str) -> List[List[int]]:
        r = re.compile(r'^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$')
        return [[int(i) for i in r.match(line).groups()] for line in puzzle_input.split('\n')]
