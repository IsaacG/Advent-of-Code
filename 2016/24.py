#!/bin/python
"""Advent of Code, Day 24: Air Duct Spelunking."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re
import string

from lib import aoc

SAMPLE = """\
###########
#0.1.....2#
#.#######.#
#4.......3#
###########"""

LineType = int
InputType = list[LineType]


class Day24(aoc.Challenge):
    """Day 24: Air Duct Spelunking."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=14),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]

    def solver(self, parsed_input: InputType, param: bool) -> int:
        floor, wires = parsed_input
        distances = collections.defaultdict(dict)
        for start, wire in wires.items():
            # self.debug(f"Build distances for {wire} at {start}")
            todo = collections.deque()
            seen = {start}
            todo.append((0, start))

            while todo:
                steps, position = todo.popleft()
                # self.debug(f"Explore {position} at {steps=}")
                if position in wires:
                    other = wires[position]
                    if other in distances[wire]:
                        assert distances[wire][other] == steps, f"{wire}-{other} == {distances[wire][other]} != {steps}"
                    distances[wire][other] = steps
                    distances[other][wire] = steps
                if len(distances[wire]) == len(wires):
                    break

                next_steps = steps + 1
                for direction in aoc.FOUR_DIRECTIONS:
                    next_pos = position + direction
                    if next_pos in seen or next_pos not in floor:
                        continue
                    todo.append((next_steps, next_pos))
                    seen.add(next_pos)

        extra = (0,) if param else tuple()

        other_wires = set(wires.values()) - {0}
        shortest = min(
            sum(
                distances[a][b]
                for a, b in zip((0,) + path, path + extra)
            )
            for path in itertools.permutations(other_wires, len(other_wires))
        )

        return shortest

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        floor = {
            complex(x, y)
            for y, line in enumerate(puzzle_input.splitlines())
            for x, char in enumerate(line)
            if char != "#"
        }
        wires = {
            complex(x, y): int(char)
            for y, line in enumerate(puzzle_input.splitlines())
            for x, char in enumerate(line)
            if char in string.digits
        }
        return floor, wires
