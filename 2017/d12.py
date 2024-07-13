#!/bin/python
"""Advent of Code, Day 12: Digital Plumber."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5""",  # 5
]

LineType = int
InputType = list[LineType]


class Day12(aoc.Challenge):
    """Day 12: Digital Plumber."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=6),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=2),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_ints_per_line

    def pipes(self, lines: list[list[int]]) -> dict[int, set[int]]:
        pipes = collections.defaultdict(set)
        for one, *others in lines:
            for other in others:
                pipes[one].add(other)
                pipes[other].add(one)
        return pipes

    def part1(self, parsed_input: InputType) -> int:
        pipes = self.pipes(parsed_input)

        # Group zero
        todo = {0}
        seen = set()
        while todo:
            cur = todo.pop()
            seen.add(cur)
            for other in pipes[cur]:
                if other not in seen:
                    todo.add(other)
        return len(seen)

    def part2(self, parsed_input: InputType) -> int:
        pipes = self.pipes(parsed_input)

        unseen = set(pipes)
        groups = 0
        while unseen:
            groups += 1
            seed = min(unseen)
            todo = {seed}
            seen = set()
            while todo:
                cur = todo.pop()
                unseen.remove(cur)
                seen.add(cur)
                for other in pipes[cur]:
                    if other not in seen:
                        todo.add(other)
        return groups

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
