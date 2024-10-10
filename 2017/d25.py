#!/bin/python
"""Advent of Code, Day 25: The Halting Problem."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = """\
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A."""

LineType = int
InputType = list[LineType]


class Day25(aoc.Challenge):
    """Day 25: The Halting Problem."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=3),
        aoc.TestCase(part=2, inputs=SAMPLE, want=aoc.TEST_SKIP),
    ]

    def solver(self, puzzle_input: InputType, part_one: bool) -> int:
        cursor = 0
        state, steps, rules = puzzle_input
        tape = set()
        for step in range(steps):
            write, move, state = rules[state][cursor in tape]
            if write:
                tape.add(cursor)
            else:
                tape.discard(cursor)
            cursor += move
        return len(tape)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        preamble, *rules = puzzle_input.split("\n\n")
        m = re.match(r"Begin in state (.)\.\nPerform a diagnostic checksum after (\d+) steps.", preamble)
        initial_state = m.group(1)
        steps = int(m.group(2))

        patt = re.compile(r"""In state (.):
  If the current value is 0:
    - Write the value ([01])\.
    - Move one slot to the (left|right)\.
    - Continue with state (.)\.
  If the current value is 1:
    - Write the value ([01])\.
    - Move one slot to the (left|right)\.
    - Continue with state (.)\.""")

        res = {}
        for rule in rules:
            start, w0, m0, n0, w1, m1, n1 = patt.match(rule).groups()
            res[start] = [
                    (w0 == "1", 1 if m0 == "right" else -1, n0),
                    (w1 == "1", 1 if m1 == "right" else -1, n1),
            ]
        return initial_state, steps, res

# vim:expandtab:sw=4:ts=4
