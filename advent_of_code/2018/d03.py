#!/bin/python
"""Day 3: Chronal Calibration.

Compute overlapping rectangles which the elves want to cut from fabric.
"""
import re
from lib import aoc


def get_overlap(data: list[list[int]]) -> set[tuple[int, int]]:
    """Calculate the overlapping squares."""
    seen_once = set()
    seen_twice = set()
    for i, x, y, w, h in data:
        for a in range(x, x + w):
            for b in range(y, y + h):
                if (a, b) in seen_once:
                    seen_twice.add((a, b))
                else:
                    seen_once.add((a, b))
    return seen_twice


def solve(data: list[list[int]], part: int) -> int:
    """Find the pattern which has no overlap with any others."""
    if part == 1:
        return len(get_overlap(data))

    seen_twice = get_overlap(data)
    for i, x, y, w, h in data:
        if all((a, b) not in seen_twice for a in range(x, x + w) for b in range(y, y + h)):
            return i
    raise RuntimeError


TESTS = []
