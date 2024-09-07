#!/bin/python
"""Advent of Code, Day 20: Particle Swarm."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>""",  # 29
    """\
p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>""",
]

LineType = int
InputType = list[LineType]


class Day20(aoc.Challenge):
    """Day 20: Particle Swarm."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=0),
        aoc.TestCase(part=2, inputs=SAMPLE[1], want=1),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    # INPUT_PARSER = aoc.parse_ints_per_line

    @staticmethod
    def distance(vals: tuple[int]) -> int:
        return sum(abs(i) for i in vals)

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        pos, vel, acc = (parsed_input[t] for t in "pva")
        # Simulate some ticks for collision removal.
        for tick in range(40 if param else 0):
            # Count positions. Any position with multiple particles is a collision.
            counts = collections.Counter(pos.values())
            collisions = {p for p, count in counts.items() if count > 1}
            # Remove particles which collided.
            pos = {idx: p for idx, p in pos.items() if p not in collisions}
            vel = {idx: v for idx, v in vel.items() if idx in pos}
            # Update velocity then position.
            vel = {idx: tuple(vel[idx][dim] + acc[idx][dim] for dim in range(3)) for idx in pos}
            pos = {idx: tuple(pos[idx][dim] + vel[idx][dim] for dim in range(3)) for idx in pos}


        if param:
            return len(pos)
        # Sort remaining particles by acceleration then velocity (Manhatten abs value).
        slowest = sorted((self.distance(acc[idx]), self.distance(vel[idx]), idx) for idx in pos)
        a, v, idx = slowest[0]
        assert idx < 775, idx
        return idx

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        data = {t: {} for t in "pva"}
        for idx, line in enumerate(puzzle_input.replace("<", "").replace(">", "").splitlines()):
            for part in line.split(", "):
                letter, numbers = part.split("=")
                data[letter][idx] = tuple(int(i) for i in numbers.split(","))
        return data

# vim:expandtab:sw=4:ts=4
