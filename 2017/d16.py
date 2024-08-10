#!/bin/python
"""Advent of Code, Day 16: Permutation Promenade."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re
import string

from lib import aoc

SAMPLE = ['s1,x3/4,pe/b', 'baedc']

LineType = int
InputType = list[LineType]


class Day16(aoc.Challenge):
    """Day 16: Permutation Promenade."""

    DEBUG = True
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=SAMPLE[1]),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_one_str

    def part1(self, parsed_input: InputType) -> int:
        size = 5 if self.testing else 16
        line = collections.deque(string.ascii_lowercase[:size])
        cmds = []
        for word in parsed_input.split(","):
            match word[0], word[1:].split("/"):
                case "s", [step]:
                    line.rotate(int(step))
                case "x", (first, second):
                    a, b = int(first), int(second)
                    line[a], line[b] = line[b], line[a]
                case "p", (first, second):
                    a, b = line.index(first), line.index(second)
                    line[a], line[b] = line[b], line[a]

        return "".join(line)

    def part2(self, parsed_input: InputType) -> int:
        size = 16
        line = collections.deque(string.ascii_lowercase[:size])
        cmds = []
        for word in parsed_input.split(","):
            match word[0], word[1:].split("/"):
                case "s", [step]:
                    cmds.append((0, int(step), 0))
                case "x", (first, second):
                    cmds.append((1, int(first), int(second)))
                case "p", (first, second):
                    cmds.append((2, first, second))

        def dance():
            for op, first, second in cmds:
                if op == 0:
                    line.rotate(first)
                elif op == 1:
                    line[first], line[second] = line[second], line[first]
                else:
                    a, b = line.index(first), line.index(second)
                    line[a], line[b] = line[b], line[a]

        dances = 1000000000
        seen = {}
        for count in range(dances):
            if count and not count % 1000:
                print(count)
            dance()
            t = tuple(line)
            if t in seen:
                remaining = (dances - 1 - count) % (count - seen[t])
                for _ in range(remaining):
                    dance()
                return "".join(line)
            seen[t] = count

        return "".join(line)

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
