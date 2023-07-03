#!/bin/python
"""Advent of Code, Day 21: Scrambled Letters and Hash."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = """\
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d"""

LineType = int
InputType = list[LineType]


class Day21(aoc.Challenge):
    """Day 21: Scrambled Letters and Hash."""

    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want="decab"),
        # aoc.TestCase(inputs=SAMPLE, part=2, want="abcde"),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_multi_str_per_line

    def part1(self, parsed_input: InputType) -> int:
        start = "abcde" if self.testing else "abcdefgh"
        data = list(start)
        for instruction in parsed_input:
            match instruction:
                case ["swap", "position", reg_x, "with", "position", reg_y]:
                    data[int(reg_x)], data[int(reg_y)] =  data[int(reg_y)], data[int(reg_x)]
                case ["swap", "letter", reg_x, "with", "letter", reg_y]:
                    swap = {reg_x: reg_y, reg_y: reg_x}
                    data = [swap.get(i, i) for i in data]
                case ["rotate", "right", reg_x, _]:
                    dist = -int(reg_x)
                    data = data[dist:] + data[:dist]
                case ["rotate", "left", reg_x, _]:
                    dist = int(reg_x)
                    data = data[dist:] + data[:dist]
                case ["rotate", "based", "on", "position", "of", "letter", reg_x]:
                    dist = data.index(reg_x)
                    dist += 2 if dist >= 4 else 1
                    dist *= -1
                    dist %= len(data)
                    data = data[dist:] + data[:dist]
                case ["reverse", "positions", reg_x, "through", reg_y]:
                    start, end = int(reg_x), int(reg_y) + 1
                    data[start:end] = reversed(data[start:end])
                case ["move", "position", reg_x, "to", "position", reg_y]:
                    data.insert(int(reg_y), data.pop(int(reg_x)))
            self.debug(instruction)
            self.debug("".join(data))
        return "".join(data)

    def part2(self, parsed_input: InputType) -> int:
        start = "decab" if self.testing else "fbgdceah"
        data = list(start)
        size = len(data)
        for instruction in reversed(parsed_input):
            self.debug(repr(instruction))
            match instruction:
                case ["swap", "position", reg_x, "with", "position", reg_y]:
                    data[int(reg_x)], data[int(reg_y)] =  data[int(reg_y)], data[int(reg_x)]
                case ["swap", "letter", reg_x, "with", "letter", reg_y]:
                    swap = {reg_x: reg_y, reg_y: reg_x}
                    data = [swap.get(i, i) for i in data]
                case ["rotate", "right", reg_x, _]:
                    dist = int(reg_x)
                    data = data[dist:] + data[:dist]
                case ["rotate", "left", reg_x, _]:
                    dist = -int(reg_x)
                    data = data[dist:] + data[:dist]
                case ["rotate", "based", "on", "position", "of", "letter", reg_x]:
                    new_pos = data.index(reg_x)
                    options = []
                    for orig_pos in range(size):
                        moved = new_pos - orig_pos
                        if moved <= 0:
                            moved += size
                        dist = (orig_pos + (2 if orig_pos >= 4 else 1)) % size
                        if dist == moved % size:
                            options.append(moved)
                    # The sample input cannot be reversed deterministically. There are multiple valid rotations.
                    assert len(options) == 1, options
                    dist = options[0]
                    data = data[dist:] + data[:dist]
                case ["reverse", "positions", reg_x, "through", reg_y]:
                    start, end = int(reg_x), int(reg_y) + 1
                    data[start:end] = reversed(data[start:end])
                case ["move", "position", reg_x, "to", "position", reg_y]:
                    data.insert(int(reg_x), data.pop(int(reg_y)))
                case _:
                    raise RuntimeError(f"Failed to parse {instruction.split()}")
            self.debug("".join(data))
        got = "".join(data)
        if not self.testing:
            assert got != "adfcgehb"
        return got

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError
