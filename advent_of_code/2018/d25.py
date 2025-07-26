#!/bin/python
"""Advent of Code, Day 25: Four-Dimensional Adventure."""
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
0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0""",  # 0
    """\
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0""",  # 12
    """\
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2""",  # 14
    """\
1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2""",  # 16
]

LineType = int
InputType = list[LineType]
log = logging.info


class Day25(aoc.Challenge):
    """Day 25: Four-Dimensional Adventure."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=2),
        # aoc.TestCase(part=1, inputs=SAMPLE[1], want=4),
        # aoc.TestCase(part=1, inputs=SAMPLE[2], want=3),
        # aoc.TestCase(part=1, inputs=SAMPLE[3], want=8),
    ]

    def part1(self, puzzle_input: InputType) -> int:
        groups = 0
        todo = set(tuple(i) for i in puzzle_input)
        while todo:
            groups += 1
            group = {todo.pop()}
            while True:
                to_add = next(
                    (
                        i for i in todo
                        if any(
                            (abs(i[0] - j[0]) + abs(i[1] - j[1]) + abs(i[2] - j[2]) + abs(i[3] - j[3]) <= 3)
                            for j in group
                        )
                    ), None
                )
                if to_add is None:
                    break
                log(f"Add {to_add} to {group}")
                group.add(to_add)
                todo.remove(to_add)
            print(groups, group)

        return groups

    # def part2(self, puzzle_input: InputType) -> int:

    # def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().input_parser(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]
        # Words: mixed str and int
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in line.split()
            )
            for line in puzzle_input.splitlines()
        ]
        # Regex splitting
        patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in patt.match(line).groups()
            )
            for line in puzzle_input.splitlines()
        ]

# vim:expandtab:sw=4:ts=4
