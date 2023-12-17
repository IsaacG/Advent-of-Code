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


class Day12(aoc.Challenge):
    """Day 12: Hot Springs."""

    PARAMETERIZED_INPUTS = [False, True]
    INPUT_PARSER = aoc.parse_one_str_per_line
    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=21),
        aoc.TestCase(inputs=SAMPLE, part=2, want=525152),
    ]

    def trim(self, springs, numbers):
        if springs and springs[0] == "":
            return self.trim(springs[1:], numbers)

        if not springs or not numbers:
            return springs, numbers

        if len(springs[0]) < numbers[0] and "#" not in springs[0]:
            return self.trim(springs[1:], numbers)

        if len(springs[-1]) < numbers[-1] and "#" not in springs[-1]:
            return self.trim(springs[:-1], numbers)

        if "#" in springs[0] and len(springs[0]) == numbers[0]:
            return self.trim(springs[1:], numbers[1:])

        mandatory_groups = tuple(group for group in springs if "#" in group)
        if len(mandatory_groups) == len(numbers) != len(springs):
            return self.trim(mandatory_groups, numbers)

        return springs, numbers

    @functools.cache
    def ways_to_fit(self, springs, numbers) -> int:
        springs, numbers = self.trim(springs, numbers)
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

    def solver(self, parsed_input: str, param: bool) -> int:
        """Return the total number of possible fits."""
        count = 0
        for line in parsed_input:
            springs_str, numbers_str = line.split()
            if param:
                springs_str = "?".join([springs_str] * 5)
                numbers_str = ",".join([numbers_str] * 5)
            springs = tuple(i for i in springs_str.split(".") if i)
            numbers = tuple(int(i) for i in numbers_str.split(","))
            count += self.ways_to_fit(springs, numbers)
        return count


# vim:expandtab:sw=4:ts=4
