#!/bin/python
"""Advent of Code, Day 1: Trebuchet?!."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""",
    """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""",
]

LineType = int
InputType = list[LineType]


class Day01(aoc.Challenge):
    """Day 1: Trebuchet?!."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=142),
        aoc.TestCase(inputs="eightwo", part=2, want=82),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=281),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_one_str_per_line

    def part1(self, parsed_input: InputType) -> int:
        c = 0
        for line in parsed_input:
            n = [int(i) for i in line if i.isdigit()]
            print(n)
            c += n[0] * 10 + n[-1]

        return c

    def part2(self, parsed_input: InputType) -> int:
        va = {a: str(b + 1) for b, a in enumerate("one two three four five six seven eight nine".split())}
        total = 0
        for line in parsed_input:
            nums = []
            for i in range(len(line)):
                if line[i:i+1].isdigit():
                    nums.append(line[i:i+1])
                else:
                    for a, b in va.items():
                        if line[i:].startswith(a):
                            nums.append(b)
            print(nums, line)
            total += int(nums[0]) * 10 + int(nums[-1])
        return total


        return
        c = 0
        va = {a: str(b + 1) for b, a in enumerate("one two three four five six seven eight nine".split())}
        for line in parsed_input:
            og = line
            line2 = line
            replace = any(i in line for i in va.keys())

            loop = True
            while loop:
                loop = False
                for i in range(len(line)):
                    for a, b in va.items():
                        if line[i:].startswith(a):
                            line = line.replace(a, str(b), 1)
                            loop = True
                            break
                    if loop:
                        break

            line2 = line[::-1]
            loop = True
            while loop:
                loop = False
                for i in range(len(line2)):
                    for a, b in va.items():
                        if line2[i:].startswith(a[::-1]):
                            line2 = line2.replace(a[::-1], str(b), 1)
                            loop = True
                            break
                    if loop:
                        break
            line2 = line2[::-1]
            print(f"{og=} {line=} {line2=}")

            n = [int(i) for i in line if i.isdigit()]
            m = [int(i) for i in line2 if i.isdigit()]
            if replace and False:
                print(og)
                print(line)
                print(f"{n[0]}{m[-1]}")
                print()
            line_num  = f"{n[0]}{m[-1]}"
            c += int(line_num)

        assert c != 55255
        return c

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
