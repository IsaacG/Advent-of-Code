#!/bin/python
"""Advent of Code, Day 10: Knot Hash."""
from __future__ import annotations

import collections
import functools
import more_itertools
import itertools
import math
import re

from lib import aoc

SAMPLE = ["3,4,1,5"]

LineType = int
InputType = list[LineType]


class Day10(aoc.Challenge):
    """Day 10: Knot Hash."""

    # PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(part=1, inputs="0", want=0),
        aoc.TestCase(part=1, inputs="4", want=6),
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=12),
        aoc.TestCase(part=2, inputs="", want="a2582a3a0e66e6e86e3812dcb672a272"),
        aoc.TestCase(part=2, inputs="AoC 2017", want="33efeb34ea91902bb2f59c9920caa6cd"),
        aoc.TestCase(part=2, inputs="1,2,3", want="3efbe78a8d82f29979031a4aa0b16a9d"),
        aoc.TestCase(part=2, inputs="1,2,4", want="63960835bcdc130f0b66d7ff4f6a5a8e"),
    ]

    INPUT_PARSER = aoc.parse_one_str

    def part1(self, parsed_input: str) -> int:
        lengths = [int(i) for i in parsed_input.split(",")]
        # self.debug(parsed_input)
        size = 5 if self.testing else 256
        data = list(range(size))
        position = 0
        for skip, length in enumerate(lengths):
            data = list(reversed(data[:length])) + data[length:]
            split = (length + skip) % size
            data = data[split:] + data[:split]
            position += length + skip
            # self.debug(f"{data=}, {length=}, {split=}, position={position % size}")
        split = size - (position % size)
        data = data[split:] + data[:split]
        result = math.prod(data[:2])
        assert len(data) == size
        if not self.testing:
            assert result < 16256
            assert result > 132
        return result

    def part2(self, parsed_input: str) -> int:
        lengths = [ord(i) for i in parsed_input] + [17, 31, 73, 47, 23]
        self.debug(f"{lengths=}")
        size = 256

        data = list(range(size))
        position = 0
        for step in range(1):
            for skip, length in enumerate(lengths * 64):
                data = list(reversed(data[:length])) + data[length:]
                split = (length + skip) % size
                data = data[split:] + data[:split]
                position += length + skip
                # self.debug(f"{data=}, {length=}, {split=}, position={position % size}")
            split = size - (position % size)
            tmp = data[split:] + data[:split]
            if step in [0, 1, 2]:
                print(f"Round {step + 1} => {tmp}")
                # return
        split = size - (position % size)
        data = data[split:] + data[:split]

        dense = [
            functools.reduce(lambda a, b: a ^ b, chunk)
            for chunk in more_itertools.chunked(data, 16)
        ]
        print(f"Dense: {dense}")
        return "".join(f"{i:02x}" for i in dense)


    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

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
