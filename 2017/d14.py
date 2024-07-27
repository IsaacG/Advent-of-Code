#!/bin/python
"""Advent of Code, Day 14: Disk Defragmentation."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re
import more_itertools

from lib import aoc
import d10

SAMPLE = "flqrgnkx"

LineType = int
InputType = list[LineType]


def tie_knots(lengths: list[int], size: int) -> list[int]:
    """Return list with knots tied at each length."""
    data = list(range(size))
    position = 0
    for skip, length in enumerate(lengths):
        # Reverse the length-span.
        data = list(reversed(data[:length])) + data[length:]
        # "Shift left" so the list starts at the position pointer.
        split = (length + skip) % size
        data = data[split:] + data[:split]
        position += length + skip

    # Shift the list based on the position so the position is actually
    # offset and not at "0".
    split = size - (position % size)
    return data[split:] + data[:split]


def knot_hash(data: str) -> str:
    nums = [ord(i) for i in data] + [17, 31, 73, 47, 23]
    data = tie_knots(nums * 64, 256)
    # Chunk and XOR in chunks of 16.
    return [
        functools.reduce(lambda a, b: a ^ b, chunk)
        for chunk in more_itertools.chunked(data, 16)
    ]


class Day14(aoc.Challenge):
    """Day 14: Disk Defragmentation."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=8108),
        aoc.TestCase(part=2, inputs=SAMPLE, want=1242),
    ]

    INPUT_PARSER = aoc.parse_one_str

    def part1(self, parsed_input: InputType) -> int:
        return sum(
            sum(i.bit_count() for i in knot_hash(f"{parsed_input}-{i}"))
            for i in range(128)
        )

    def part2(self, parsed_input: InputType) -> int:
        for pos_y in range(8):
            line_input = f"{parsed_input}-{pos_y}"
            hashed = knot_hash(line_input)
            print(line_input, "".join(f"{i:02x}" for i in hashed)[:8], "".join(f"{i:b}" for i in hashed)[:8])
        used = {
            complex(pos_x, pos_y)
            for pos_y in range(128)
            for pos_x, val in enumerate("".join([f"{i:08b}" for i in knot_hash(f"{parsed_input}-{pos_y}")]))
            if val == "1"
        }
        for pos_y in range(8):
            line = ["#" if complex(pos_x, pos_y) in used else "." for pos_x in range(8)]
            print("".join(line))
        print(len(used))
        count = 0
        while used:
            todo = {used.pop()}
            count += 1
            while todo:
                cur = todo.pop()
                for neighbor in aoc.neighbors(cur):
                    if neighbor in used:
                        used.remove(neighbor)
                        todo.add(neighbor)
        return count

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError
