#!/bin/python
"""Advent of Code, Day 17: Two Steps Forward."""
from __future__ import annotations

import collections
import functools
import itertools
import hashlib
import math
import re

from lib import aoc

SAMPLE = [
    ('ihgpwlah', 'DDRRRD', 370),
    ('kglvqrro', 'DDUDRLRRUDRD', 492),
    ('ulqzkmiv', 'DRURDRUDDLLDLUURRDULRLDUUDDDRR', 830),
]

LineType = int
InputType = list[LineType]


class Day17(aoc.Challenge):
    """Day 17: Two Steps Forward."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=s[0], part=1, want=s[1]) for s in SAMPLE
    ] + [
        aoc.TestCase(inputs=s[0], part=2, want=s[2]) for s in SAMPLE
    ]

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        seen = {""}
        todo = collections.deque()
        todo.append(("", 0, 0))

        dirs = {"L": (-1, 0), "R": (1, 0), "D": (0, 1), "U": (0, -1)}
        doors = "UDLR"
        open = "bcdef"
        longest = 0

        def options(steps) -> list[str]:
            keys = hashlib.md5((parsed_input + steps).encode()).hexdigest()[:4]
            return [door for door, key in zip(doors, keys) if key in open]

        while todo:
            steps, cur_x, cur_y = todo.popleft()
            if cur_x == 3 and cur_y == 3:
                step_count = len(steps)
                if step_count > longest:
                    longest = step_count
                if param:
                    continue
                else:
                    return steps
            for option in options(steps):
                d_x, d_y = dirs[option]
                next_x, next_y = cur_x + d_x, cur_y + d_y
                if 0 <= next_x < 4 and 0 <= next_y < 4:
                    next_steps = steps + option
                    if next_steps in seen:
                        continue
                    seen.add(next_steps)
                    todo.append((next_steps, next_x, next_y))

        return longest
