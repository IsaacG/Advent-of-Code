#!/bin/python
"""Advent of Code, Day 14: Chocolate Charts."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = ["9", "5", "18", "2018"]

LineType = int
InputType = list[LineType]


class Day14(aoc.Challenge):
    """Day 14: Chocolate Charts."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs="9", part=1, want="5158916779"),
        aoc.TestCase(inputs="5", part=1, want="0124515891"),
        aoc.TestCase(inputs="18", part=1, want="9251071085"),
        aoc.TestCase(inputs="2018", part=1, want="5941429882"),
        aoc.TestCase(inputs="51589", part=2, want=9),
        aoc.TestCase(inputs="01245", part=2, want=5),
        aoc.TestCase(inputs="92510", part=2, want=18),
        aoc.TestCase(inputs="59414", part=2, want=2018),
    ]

    INPUT_PARSER = aoc.parse_one_str

    def part1(self, parsed_input: str) -> int:
        stop = int(parsed_input) + 10
        recipes = [3, 7]
        elf1, elf2 = 0, 1
        count = 2
        while count < stop:
            # print(recipes)
            v1, v2 = recipes[elf1], recipes[elf2]
            new = v1 + v2
            if new >= 10:
                recipes.append(1)
                count += 1
            recipes.append(new % 10)
            count += 1

            elf1, elf2 = (elf1 + 1 + v1) % count, (elf2 + 1 + v2) % count
        return "".join(str(i) for i in recipes[int(parsed_input):int(parsed_input) + 10])

    def part2(self, parsed_input: InputType) -> int:
        # stop = parsed_input + 10
        want = [int(i) for i in parsed_input]
        want_len = len(parsed_input)

        recipes = [3, 7]
        elf1, elf2 = 0, 1
        count = 2

        while count < 100000000:
            # print(recipes)
            v1, v2 = recipes[elf1], recipes[elf2]
            new = v1 + v2
            if new >= 10:
                recipes.append(1)
                count += 1
                if recipes[-want_len:] == want:
                    return count - want_len
            recipes.append(new % 10)
            count += 1
            if recipes[-want_len:] == want:
                return count - want_len

            elf1, elf2 = (elf1 + 1 + v1) % count, (elf2 + 1 + v2) % count

