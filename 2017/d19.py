#!/bin/python
"""Advent of Code, Day 19: A Series of Tubes."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re
import string

from lib import aoc

SAMPLE = [
    """\
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+""",  # 3
    'ABCDEF',  # 11
]

LineType = int
InputType = list[LineType]


class Day19(aoc.Challenge):
    """Day 19: A Series of Tubes."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=SAMPLE[1]),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=38),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_ascii_char_map(lambda x: None if x == " " else x)

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        direction = complex(0, 1)
        pipes = {complex(0, 1): "|" + string.ascii_letters, complex(1, 0): "-" + string.ascii_letters}
        pipes |= {-d: v for d, v in pipes.items()}
        rotate = {d: {d * 1j, d * -1j} for d in aoc.FOUR_DIRECTIONS}
        maze = parsed_input
        location = next(i for i in maze if i.imag == 0)
        result = []
        for step in itertools.count(1):
            cur_char = maze[location]
            if cur_char in string.ascii_letters:
                result.append(cur_char)
            next_location = location + direction
            if cur_char == "+" and maze.get(next_location) != pipes[direction]:
                want_pipe = pipes[direction * 1j]
                direction = next(d for d in rotate[direction] if location + d in maze and maze[location + d] in want_pipe)
            location += direction
            if location not in maze:
                return step if param else "".join(result)

# vim:expandtab:sw=4:ts=4
