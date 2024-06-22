#!/bin/python
"""Advent of Code, Day 9: Stream Processing."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = (
    [
        ('{}', '1'),
        ('{{{}}}', '6'),
        ('{{},{}}', '5'),
        ('{{{},{},{{}}}}', '16'),
        ('{<a>,<a>,<a>,<a>}', '1'),
        ('{{<ab>},{<ab>},{<ab>},{<ab>}}', '9'),
        ('{{<!!>},{<!!>},{<!!>},{<!!>}}', '9'),
        ('{{<a!>},{<a!>},{<a!>},{<ab>}}', '3'),
    ],
    [
        ('<>', 0),
        ('<random characters>', 17),
        ('<<<<>', 3),
        ('<{!>}>', 2),
        ('<!!>', 0),
        ('<!!!>>', 0),
        ('<{o"i!a,<{i<a>', 10),
    ]
)


class Day09(aoc.Challenge):
    """Day 9: Stream Processing."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    SUBMIT = {1: False, 2: False}
    PARAMETERIZED_INPUTS = [0, 1]

    TESTS = [
        aoc.TestCase(inputs=data, part=part, want=int(val))
        for part, pairs in enumerate(SAMPLE, 1)
        for data, val in pairs
    ]
    INPUT_PARSER = aoc.parse_one_str

    def solver(self, parsed_input: str, param) -> int | str:
        stream = iter(parsed_input)

        total = 0
        score = 0
        garbage = False
        garbage_count = 0

        while True:
            try:
                char = next(stream)
            except StopIteration:
                break
            if char == "!":
                next(stream)
            elif garbage:
                if char == ">":
                    garbage = False
                else:
                    garbage_count += 1
            elif char == "<":
                garbage = True
            elif char == "{":
                score += 1
            elif char == "}":
                total += score
                score -= 1

        return (total, garbage_count)[param]


# vim:expandtab:sw=4:ts=4
