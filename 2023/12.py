#!/bin/python
"""Advent of Code, Day 12: Hot Springs."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

LineType = int
InputType = list[LineType]


class Day12(aoc.Challenge):
    """Day 12: Hot Springs."""

    DEBUG = False
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs="??? 1", part=1, want=3),
        aoc.TestCase(inputs="?#?#?#?#?#?#?#? 1,3,1,6", part=1, want=1),
        aoc.TestCase(inputs="????.#...#... 4,1,1", part=1, want=1),
        aoc.TestCase(inputs="????.######..#####. 1,6,5", part=1, want=4),
        aoc.TestCase(inputs="?###???????? 3,2,1", part=1, want=10),
        aoc.TestCase(inputs="??.?? 1,1", part=1, want=4),
        aoc.TestCase(inputs=SAMPLE, part=1, want=21),
        aoc.TestCase(inputs=SAMPLE, part=2, want=0),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def possibilities_one(self, group: str):
        if group == "":
            yield []
        elif "?" not in group:
            yield [group]
        else:
            repl = group.replace("?", "#", 1)
            yield from self.possibilities_one(repl)
            a, b = group.split("?", 1)
            if a and b:
                for x, y in itertools.product(self.possibilities_one(a), self.possibilities_one(b)):
                    yield x + y
            elif a:
                yield from self.possibilities_one(a)
            elif b:
                yield from self.possibilities_one(b)
            else:
                yield []

    def is_match(self, springs, numbers) -> int:
        springs = list(itertools.chain.from_iterable(springs))
        return len(springs) == len(numbers) and all(len(group) == number for group, number in zip(springs, numbers))

    def possibilities_many(self, groups):
        options = []
        for group in groups:
            group_options = []
            for i in self.possibilities_one(group):
                group_options.append(i)

            # options.append(list(itertools.chain.from_iterable(group_options)))
            options.append(group_options)
        self.debug(f"Per group options: {groups}, {options}")
        product = list(itertools.product(*options))
        self.debug(f"{product=}")
        yield from product

    def solve_p(self, springs, numbers) -> int:
        while springs and numbers and len(springs[0]) == numbers[0]:
            springs, numbers = springs[1:], numbers[1:]
        while springs and numbers and len(springs[-1]) == numbers[-1]:
            springs, numbers = springs[:-1], numbers[:-1]
        if not numbers and not springs:
            return 1
        if not numbers and not any("#" in s for s in springs):
            return 1
        if not numbers or not springs:
            return 0
        
        self.debug(f"Solve: {springs=}, {numbers=}")
        count = 0
        for groups in self.possibilities_many(springs):
            good = self.is_match(groups, numbers)
            self.debug(f"{good=}, {groups=}, {numbers=}")
            if good: count+=1
        return count

    def part1(self, parsed_input: InputType) -> int:
        got = sum(self.solve_p(springs, numbers) for springs, numbers in parsed_input)
        assert got > 6863
        return got

    def part2(self, parsed_input: InputType) -> int:
        raise NotImplementedError

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        lines = []
        for line in puzzle_input.splitlines():
            springs, numbers = line.split()
            lines.append(
                (
                    [i for i in springs.split(".") if i],
                    [int(i) for i in numbers.split(",")],
                )
            )
        return lines
