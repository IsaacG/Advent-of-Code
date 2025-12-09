#!/bin/python
"""Advent of Code, Day 9: Movie Theater."""
from __future__ import annotations

import collections
import functools
import itertools
import logging
import math
import re

from lib import aoc

SAMPLE = [
    """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3""",  # 0
]

LineType = int
InputType = list[LineType]
log = logging.info


class Day09(aoc.Challenge):
    """Day 9: Movie Theater."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=50),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=24),
    ]

    def part1(self, puzzle_input: InputType) -> int | str:
        return max(
            (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            for (x1, y1), (x2, y2) in itertools.combinations(puzzle_input, 2)
        )

    def part2(self, puzzle_input: InputType) -> int | str:
        if puzzle_input[0][0] == puzzle_input[1][0]:
            points = puzzle_input[-1:] + puzzle_input
        else:
            points = puzzle_input + puzzle_input[:1]

        assert len(points) % 2 == 1
        # y, x1, x2
        horiz = []
        for i in range(0, len(points) - 1, 2):
            x1, x2, y = *sorted([points[i][0], points[i+1][0]]), points[i][1]
            assert x1 != x2, f"{i=}, {x1=}, {x2=}"
            assert y == points[i+1][1]
            horiz.append((y, x1, x2))
        horiz.sort()
        # x, y1, y2
        vert = []
        for i in range(1, len(points), 2):
            y1, y2, x = *sorted([points[i][1], points[i+1][1]]), points[i][0]
            assert y1 != y2
            vert.append((x, y1, y2))
        vert.sort()
        assert len(horiz) == len(vert)
        assert len(horiz) == len(puzzle_input) / 2
        heights = sorted(y for y, _, _ in horiz)

        """
        ranges = {}
        for h in heights:
            edges = []
            inside = False
            for (x, y1, y2) in vert:
                if not y1 <= h < y2:
                    continue
                edges.append(x)



            min_h = max(h for h in heights if h <= top)
            max_h = min(h for h in heights if h >= bottom)
            insidew = {h: [] for h in heights}
            insides = {h: [] for h in heights}
            for (x, y1, y2) in (vert):
                pass


        def valid(x1, y1, x2, y2):
            left, right = sorted((x1, x2))
            top, bottom = sorted((y1, y2))

            inside = False
            intrusions = []
            for idx, (x, y1, y2) in enumerate(vert):
                if y2 < top or y1 > bottom:
                    continue
                if y1 <= top and y2 >= bottom:
                    inside = not inside
                else:
                    intrusions.append((x, y1, y2))
                if x > left and not inside:
                    return False
                if x >= right:
                    if not inside:
                        return False
                    break
                return inside
                """

        best = 0

        def valid(x1, y1, x2, y2):
            nonlocal best
            size = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if size < best:
                return False
            top, bottom = sorted([y1, y2])
            left, right = sorted([x1, x2])

            for (y, x1, x2) in horiz:
                if not top < y < bottom:
                    continue
                if x1 >= right or x2 <= left:
                    continue
                return False
            for (x, y1, y2) in vert:
                if not left < x < right:
                    continue
                if y1 >= bottom or y2 <= top:
                    continue
                return False
            best = size
            return True



        got = max(
            (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            for (x1, y1), (x2, y2) in itertools.combinations(puzzle_input, 2)
            if valid(x1, y1, x2, y2)
        )
        assert got not in [127844949, 3372009, 117097056, 4602673662, 4746238001], got
        return got

# vim:expandtab:sw=4:ts=4
