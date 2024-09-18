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
STATES_P1 = [CLEAN, INFECTED, CLEAN]
STATES_P2 = [CLEAN, WEAKENED, INFECTED, FLAGGED, CLEAN]
ROTATIONS = {CLEAN: 1j, WEAKENED: 1, INFECTED: -1j, FLAGGED: -1}


class Day22(aoc.Challenge):
    """Day 22: Sporifica Virus."""

    INPUT_PARSER = aoc.ParseMultiple(
        [
            aoc.Transform(lambda x: len(x.splitlines())),
            aoc.parse_ascii_bool_map("#", origin_top_left=False),
        ]
    )
    PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=5587),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=2511944),
    ]

    def solver(self, parsed_input: list[list[int]], param: bool) -> int:
        dimension, initial_infected = parsed_input
        board = {i: INFECTED for i in initial_infected}
        states = STATES_P2 if param else STATES_P1
        next_state = {a: b for a, b in zip(states[:-1], states[1:])}
        direction = complex(0, 1)
        location = complex(1, 1) * ((dimension - 1) // 2)
        infected = 0
        for step in range(10000000 if param else 10000):
            state = board.get(location, CLEAN)
            direction *= ROTATIONS[state]
            board[location] = next_state[state]
            if board[location] == INFECTED:
                infected += 1
            location += direction

        return infected

# vim:expandtab:sw=4:ts=4
