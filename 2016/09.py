#!/bin/python
"""Advent of Code, Day 9: Explosives in Cyberspace."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    ('ADVENT', 'ADVENT'),
    ('A(1x5)BC', 'ABBBBBC'),
    ('(3x3)XYZ', 'XYZXYZXYZ'),
    ('A(2x2)BCD(2x2)EFG', 'ABCBCDEFEFG'),
    ('(6x1)(1x3)A', '(1x3)A'),
    ('X(8x2)(3x3)ABCY', 'X(3x3)ABC(3x3)ABCY'),
    ('(3x3)XYZ', len('XYZXYZXYZ')),
    ('X(8x2)(3x3)ABCY', len('XABCABCABCABCABCABCY')),
    ('(27x12)(20x12)(13x14)(7x10)(1x12)A', 241920),
    ('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN', 445),
]

LineType = int
InputType = list[LineType]


class Day09(aoc.Challenge):
    """Day 9: Explosives in Cyberspace."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=i[0], part=1, want=len(i[1])) for i in SAMPLE[:6]
    ] + [
        aoc.TestCase(inputs=i[0], part=2, want=i[1]) for i in SAMPLE[6:]
    ]

    INPUT_PARSER = aoc.parse_one_str

    def part1(self, parsed_input: InputType) -> int:
        out = []
        data = list(reversed(parsed_input))

        while data:
            char = data.pop()
            if char != "(":
                out.append(char)
            else:
                buf = []
                while (char := data.pop()) != ")":
                    buf.append(char)
                count, repeat = "".join(buf).split("x")
                buf = "".join(data.pop() for _ in range(int(count)))
                out.append(buf * int(repeat))

        return len("".join(out))

    def seq_len(self, sequence: str) -> int:
        count = 0
        data = list(reversed(sequence))

        while data:
            char = data.pop()
            if char != "(":
                count += 1
            else:
                buf = []
                while (char := data.pop()) != ")":
                    buf.append(char)
                sub_count, repeat = "".join(buf).split("x")
                sub_sequence = "".join(data.pop() for _ in range(int(sub_count)))
                count += int(repeat) * self.seq_len(sub_sequence)

        return count

    def part2(self, parsed_input: InputType) -> int:
        return self.seq_len(parsed_input)


    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError
