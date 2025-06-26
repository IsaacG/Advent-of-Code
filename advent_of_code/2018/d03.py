#!/bin/python
"""Day 1: Chronal Calibration.

Compute overlapping rectangles which the elves want to cut from fabric.
"""

import re
from typing import List, Set, Tuple

from lib import aoc


class Day03(aoc.Challenge):

    def get_overlap(self, puzzle_input: List[List[int]]) -> Set[Tuple[int, int]]:
        """Calculate the overlapping squares."""
        seen_once = set()
        seen_twice = set()
        for i, x, y, w, h in puzzle_input:
            for a in range(x, x + w):
                for b in range(y, y + h):
                    if (a, b) in seen_once:
                        seen_twice.add((a, b))
                    else:
                        seen_once.add((a, b))
        return seen_twice

    def part1(self, puzzle_input: List[List[int]]) -> int:
        return len(self.get_overlap(puzzle_input))

    def part2(self, puzzle_input: List[List[int]]) -> int:
        """Find the pattern which has no overlap with any others."""
        seen_twice = self.get_overlap(puzzle_input)

        for i, x, y, w, h in puzzle_input:
            if all((a, b) not in seen_twice for a in range(x, x + w) for b in range(y, y + h)):
                return i
        raise RuntimeError
