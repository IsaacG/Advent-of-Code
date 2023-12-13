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
        print(f"{args[1:]} => {got}")
        return got
    return inner

class Day12(aoc.Challenge):
    """Day 12: Hot Springs."""

    DEBUG = True
    DEBUG = False
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs="??###?##.??????#??# 8,1,2,2", part=1, want=4),
        aoc.TestCase(inputs=SAMPLE, part=1, want=21),
        aoc.TestCase(inputs="??? 1", part=1, want=3),
        aoc.TestCase(inputs="?#?#?#?#?#?#?#? 1,3,1,6", part=1, want=1),
        aoc.TestCase(inputs="????.#...#... 4,1,1", part=1, want=1),
        aoc.TestCase(inputs="????.######..#####. 1,6,5", part=1, want=4),
        aoc.TestCase(inputs="?###???????? 3,2,1", part=1, want=10),
        aoc.TestCase(inputs="??.?? 1,1", part=1, want=4),
        aoc.TestCase(inputs=SAMPLE, part=2, want=0),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def is_match(self, springs, numbers) -> int:
        return len(springs) == len(numbers) and all(len(group) == number for group, number in zip(springs, numbers))

    def trim(self, springs, numbers) -> int:
        self.debug(f"{springs=} {numbers=}")
        if springs and numbers:
            if "#" in springs[0] and len(springs[0]) == numbers[0]:
                return self.trim(springs[1:], numbers[1:])
            if "#" in springs[-1] and len(springs[-1]) == numbers[-1]:
                return self.trim(springs[:-1], numbers[:-1])
            # ["#???"], [2] => ["?"], []
            if springs[0].startswith("#") and "." not in springs[:numbers[0]]:
                return self.trim([springs[0][numbers[0]:].removeprefix("?")] + springs[1:], numbers[1:])
            # ["???#"], [2] => ["?"], []
            if springs[-1].endswith("#") and "." not in springs[-1][:-numbers[0]]:
                return self.trim(springs[:-1] + [springs[-1][:-numbers[-1]].removesuffix("?")], numbers[:-1])

        return springs, numbers

    def split(self, springs, numbers):
        if len(springs) <= 1 or len(numbers) <= 1:
            return None

        first_num, second_num = sorted(numbers, reverse=True)[:2]
        if first_num == second_num:
            return None

        if False:
            # (['?', '???', '??'], [3, 1]) => [(['?'], []), (['??'], [1])]
            springs_len = [len(group) for group in springs]
            first_len, second_len = sorted(springs_len, reverse=True)[:2]
            if first_len > second_len and first_len == first_num:
                num_idx = numbers.index(first_num)
                springs_idx = springs_len.index(first_num)
                return [(springs[:springs_idx], numbers[:num_idx]), (springs[springs_idx + 1:], numbers[num_idx + 1:])]

            # (['?', '?##', '???'], [3, 1]) => [(['?'], []), (['???'], [1])]
            want = "#" * (second_num + 1)
            for idx, group in enumerate(springs):
                if len(group) == first_num and want in group:
                    num_idx = numbers.index(first_num)
                    return [(springs[:idx], numbers[:num_idx]), (springs[idx + 1:], numbers[num_idx + 1:])]

        # (['?', '??###???', '?'], [3, 1]) => [(['?', '?'], []), ([??', '?'], [1])]
        want = "#" * first_num
        for idx, group in enumerate(springs):
            if want in group:
                num_idx = numbers.index(first_num)
                pre, post = [(springs[:idx], numbers[:num_idx]), (springs[idx + 1:], numbers[num_idx + 1:])]
                group_pre, group_post = group.split(want, 1)
                group_pre = group_pre.removesuffix("?")
                group_post = group_post.removeprefix("?")
                if group_pre:
                    pre[0].append(group_pre)
                if group_post:
                    post[0].insert(0, group_post)
                return pre, post

        return None

    # @print_io
    def ways_to_fit(self, springs, numbers) -> int:
        springs, numbers = self.trim(springs, numbers)
        if not numbers:
            if not springs or not any("#" in s for s in springs):
                return 1
            if springs:
                raise ValueError(f"Cannot fit {springs} {numbers}")
        if not springs:
            raise ValueError(f"Cannot fit {springs} {numbers}")
        if self.is_match(springs, numbers):
            return 1
        # if len(springs) == 1 and len(numbers) == 1 and "#" not in springs[0]:
        #     return len(springs[0]) - numbers[0] + 1
        if len(springs) == 1 and len(springs[0]) == sum(numbers) + len(numbers) - 1:
            return 1

        if (split := self.split(springs, numbers)):
            a, b = split
            return self.ways_to_fit(*a) * self.ways_to_fit(*b)
        
        springs_str = ".".join(springs)
        size = numbers[0]
        count = 0

        end = len(springs_str) - sum(numbers[1:]) - len(numbers)
        end = min(end, len(springs_str) - size)
        if "#" in springs_str:
            end = min(springs_str.index("#"), end)
        for start in range(end + 1):
            assert len(springs_str) >= start + size
            if "." not in springs_str[start:start + size] and (len(springs_str) == start + size or springs_str[start + size] != "#"):
                try:
                    count += self.ways_to_fit(
                        [i for i in springs_str[start + size + 1:].split(".") if i],
                        numbers[1:]
                    )
                except:
                    pass
        self.debug(f"Ways to fit {springs_str} {numbers}: {count}")
        return count

    def part1(self, parsed_input: InputType) -> int:
        for springs, numbers in parsed_input:
            self.debug(f"{'.'.join(springs)} {','.join(str(i) for i in numbers)}")
            self.debug(f" => {self.ways_to_fit(springs, numbers)}")
            print(f"{'.'.join(springs)} {','.join(str(i) for i in numbers)} {self.ways_to_fit(springs, numbers)}")
        got = sum(self.ways_to_fit(springs, numbers) for springs, numbers in parsed_input)
        if not self.testing:
            assert got > 6863
            assert got > 7221
            assert got > 7409
            assert got != 7661
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
