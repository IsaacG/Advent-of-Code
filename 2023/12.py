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


def print_io(func):
    def inner(*args):
        got = func(*args)
        print(f"{func.__name__}{args} => {got}")
        return got
    return inner


# @print_io
def trim(springs, numbers):
    if springs and springs[0] == "":
        return trim(springs[1:], numbers)

    if not springs or not numbers:
        return springs, numbers

    if len(springs[0]) < numbers[0] and "#" not in springs[0]:
        return trim(springs[1:], numbers)

    if len(springs[-1]) < numbers[-1] and "#" not in springs[-1]:
        return trim(springs[:-1], numbers)

    if "#" in springs[0] and len(springs[0]) == numbers[0]:
        return trim(springs[1:], numbers[1:])

    mandatory_groups = tuple(group for group in springs if "#" in group)
    if len(mandatory_groups) == len(numbers) != len(springs):
        return trim(mandatory_groups, numbers)

    return springs, numbers


class Day12(aoc.Challenge):
    """Day 12: Hot Springs."""

    DEBUG = True
    DEBUG = False
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    PARAMETERIZED_INPUTS = [False, True]
    INPUT_PARSER = aoc.parse_one_str_per_line

    TESTS = [
        aoc.TestCase(inputs="??###?##.??????#??# 8,1,2,2", part=1, want=4),
        aoc.TestCase(inputs=SAMPLE, part=1, want=21),
        aoc.TestCase(inputs="??? 1", part=1, want=3),
        aoc.TestCase(inputs="#?? 1", part=1, want=1),
        aoc.TestCase(inputs="?#? 1", part=1, want=1),
        aoc.TestCase(inputs="??# 1", part=1, want=1),
        aoc.TestCase(inputs="?#?#?#?#?#?#?#? 1,3,1,6", part=1, want=1),
        aoc.TestCase(inputs="????.#...#... 4,1,1", part=1, want=1),
        aoc.TestCase(inputs="????.######..#####. 1,6,5", part=1, want=4),
        aoc.TestCase(inputs="?###???????? 3,2,1", part=1, want=10),
        aoc.TestCase(inputs="??.?? 1,1", part=1, want=4),
        aoc.TestCase(inputs="???.### 1,1,3", part=2, want=1),
        # Part 2
        # aoc.TestCase(inputs="?#?#?#?#?#?#?#? 1,3,1,6", part=2, want=1),
        # aoc.TestCase(inputs=".??..??...?##. 1,1,3", part=2, want=16384),
        # aoc.TestCase(inputs="????.#...#... 4,1,1", part=2, want=16),
        # aoc.TestCase(inputs="????.######..#####. 1,6,5", part=2, want=2500),
        # aoc.TestCase(inputs="?###???????? 3,2,1", part=2, want=506250),
        aoc.TestCase(inputs=SAMPLE, part=2, want=525152),
    ]

    # @print_io
    @functools.cache
    def ways_to_fit(self, springs, numbers) -> int:
        springs, numbers = trim(springs, numbers)
        if not springs and not numbers:
            # Nothing left, all fit. Done.
            self.debug("ways_to_fit: nothing left, one fit")
            return 1
        elif not springs:
            # Unmatched numbers. Cannot fit.
            self.debug("ways_to_fit: no more springs, zero fit")
            return 0
        elif not numbers:
            if any("#" in group for group in springs):
                # Unmatched # is a failure.
                self.debug("ways_to_fit: unmatched springs, zero fit")
                return 0
            else:
                self.debug("ways_to_fit: no more numbers, one fit")
                return 1
        elif "#" in springs[0] and len(springs[0]) < numbers[0]:
            self.debug("ways_to_fit: first spring group cannot match")
            return 0

        if len(numbers) == 1:
            if all("#" not in group for group in springs):
                number = numbers[0]
                return sum(
                    len(group) - number + 1
                    for group in springs
                    if len(group) >= number
                )

        count = 0
        if springs[0].startswith("?"):
            skip_start = (springs[0][1:],) + springs[1:]
            count += self.ways_to_fit(skip_start, numbers)

        first_group = springs[0]
        first_num = numbers[0]

        assert len(first_group) >= first_num

        if len(first_group) == first_num:
            count += self.ways_to_fit(springs[1:], numbers[1:])
        elif len(first_group) > first_num:
            if first_group[first_num] == "?":
                at_start = (first_group[first_num + 1:],) + springs[1:]
                count += self.ways_to_fit(at_start, numbers[1:])

        self.debug(f"Ways to fit {springs} {numbers}: {count}")
        return count

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        count = 0
        line_count = len(parsed_input)
        for idx, line in enumerate(parsed_input):
            springs_str, numbers_str = line.split()
            if param:
                springs_str = "?".join([springs_str] * 5)
                numbers_str = ",".join([numbers_str] * 5)
            springs = tuple(i for i in springs_str.split(".") if i)
            numbers = tuple(int(i) for i in numbers_str.split(","))
            count += self.ways_to_fit(springs, numbers)
            # print(f"{idx:02}/{line_count:02}: {line:40} => {count:6}")
        return count


if __name__ == "__main__":
    d = Day12(2023)
    data = SAMPLE.splitlines() + [
        ".??##????? 3,1",
        ".?.###.??? 3,1",
        ".?.?##.??? 3,1",
        "..????..?? 3,1",
        ".?.???..?? 3,1",
        "?.??###???.? 3,1",
    ]
    for line in data:
        parsed = d.input_parser(line)[0]
        print(parsed, "=>", d.ways_to_fit(*parsed))

# vim:expandtab:sw=4:ts=4
