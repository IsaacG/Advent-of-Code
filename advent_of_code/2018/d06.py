#!/bin/python
"""Advent of Code, Day 6: Chronal Coordinates."""
from __future__ import annotations

import collections
import functools
import itertools
import logging
import math
import re
import string

from lib import aoc

SAMPLE = [
    """\
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""",
]

LineType = int
InputType = list[LineType]


def log(*args, **kwargs) -> None:
    logging.info(*args, **kwargs)

class Day06(aoc.Challenge):
    """Day 6: Chronal Coordinates."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=17),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=16),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_ints

    def part1(self, puzzle_input: InputType) -> int:
        min_x, min_y = -1, -1
        max_x = max(x for x, y in puzzle_input) + 1
        max_y = max(y for x, y in puzzle_input) + 1
        groups = [{complex(x, y),} for x, y in puzzle_input]
        claimed = {complex(x, y) for x, y in puzzle_input}
        equadistance = set()
        unbounded = set()
        found_more = True

        def show():
            return
            mp = {
                p : l
                for l, g in zip(string.ascii_lowercase, groups)
                for p in g
            }
            for x, y in puzzle_input:
                mp[complex(x, y)] = mp[complex(x, y)].upper()
            for y in range(min_y, max_y + 1):
                print("".join(mp.get(complex(x, y), "_" if complex(x, y) in equadistance else ".") for x in range(min_x, max_x + 1)))
            print()


        while found_more:
            show()
            found_more = False
            expanded = [
                ({p + d for p in group for d in aoc.FOUR_DIRECTIONS}) - equadistance - claimed
                for group in groups
            ]
            counts = collections.Counter(p for group in expanded for p in group)
            equadistance.update(p for p, c in counts.items() if c > 1)
            for idx, (group, n) in enumerate(zip(groups, expanded)):
                new_points = n - equadistance
                claimed.update(new_points)
                on_map = {p for p in new_points if min_x <= p.real <= max_y and min_y <= p.imag <= max_y}
                if len(on_map) != len(new_points):
                    unbounded.add(idx)
                if on_map:
                    group.update(on_map)
                    found_more = True
        print(unbounded)
        return max(len(group) for idx, group in enumerate(groups) if idx not in unbounded)

    def part2(self, puzzle_input: InputType) -> int:
        distance = 32 if self.testing else 10000
        min_x = min(x for x, y in puzzle_input)
        max_x = max(x for x, y in puzzle_input)
        min_y = min(y for x, y in puzzle_input)
        max_y = max(y for x, y in puzzle_input)

        def sum_distance(x, y):
            return sum(abs(x - px) + abs(y - py) for px, py in puzzle_input)

        return = sum(
            sum_distance(x, y) < distance
            for x in range(min_x, max_x + 1)
            for y in range(min_y, max_y + 1)
        )


# vim:expandtab:sw=4:ts=4
