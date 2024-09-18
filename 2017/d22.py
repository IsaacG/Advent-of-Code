#!/bin/python
"""Advent of Code, Day 22: Sporifica Virus."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
..#
#..
...""",  # 2
]

LineType = int
InputType = list[LineType]

CLEAN, WEAKENED, INFECTED, FLAGGED = range(4)


class Day22(aoc.Challenge):
    """Day 22: Sporifica Virus."""

    INPUT_PARSER = aoc.ParseMultiple(
        [
            aoc.Transform(lambda x: len(x.splitlines())),
            aoc.parse_ascii_bool_map("#"),
        ]
    )

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=5587),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=2511944),
    ]

    def part1(self, parsed_input: InputType) -> int:
        dimension, board = parsed_input
        center = (dimension - 1) // 2
        direction = complex(0, -1)
        location = complex(1, 1) * center
        infected = 0
        for step in range(10000):
            is_infected = location in board
            if not is_infected:
                infected += 1
            direction *= 1j if is_infected else -1j
            (board.remove if is_infected else board.add)(location)
            location += direction

        return infected

    def part2(self, parsed_input: InputType) -> int:
        dimension, initial_infected = parsed_input
        board = {i: INFECTED for i in initial_infected}
        rotations = {CLEAN: -1j, WEAKENED: 1, INFECTED: 1j, FLAGGED: -1}
        center = (dimension - 1) // 2
        direction = complex(0, -1)
        location = complex(1, 1) * center
        infected = 0
        for step in range(10000000):
            state = board.get(location, CLEAN)
            direction *= rotations[state]
            board[location] = (state + 1) % 4
            if board[location] == INFECTED:
                infected += 1
            location += direction

        return infected

# vim:expandtab:sw=4:ts=4
