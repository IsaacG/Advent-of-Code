#!/bin/python
"""Advent of Code: Day 11."""

import collections
import functools
import math
import string
import re

import typer
from lib import aoc

SAMPLE = ["abcdefgh", "ghijklmn"]

LineType = int
InputType = list[LineType]
NOT_ALLOWED = {string.ascii_lowercase.index(i) for i in "iol"}


def parts(num: int) -> list[int]:
    parts = []
    for i in range(8):
        num, b = divmod(num, 26)
        parts.append(b)
    parts.reverse()
    return parts


def valid(password: str) -> bool:
    if any(i in password for i in NOT_ALLOWED):
        return False
    if not any(password[i] + 2 == password[i + 1] + 1 == password[i + 2] for i in range(6)):
        return False

    overlaps = 0
    i = 0
    while i < 7:
        if password[i] == password[i + 1]:
            i += 1
            overlaps += 1
        i += 1
    return overlaps > 1


class Day11(aoc.Challenge):
    """Day 11: Corporate Policy."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want="abcdffaa"),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want="ghjaabcc"),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want="abcdffbb"),
    ]

    INPUT_TYPES = str

    def next_password(self, password: str) -> str:
        num = 0
        for char in password:
            num *= 26
            num += string.ascii_lowercase.index(char)
        num += 1
        while not valid(parts(num)):
            num += 1

        password = "".join(string.ascii_lowercase[i] for i in parts(num))
        return password

    def part1(self, parsed_input: InputType) -> int:
        assert valid(parts(334140716))  # abcdffaa
        assert valid(parts(50460204602))  # ghjaabcc

        return self.next_password(parsed_input)

    def part2(self, parsed_input: InputType) -> int:
        password = self.next_password(parsed_input)
        return self.next_password(password)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return puzzle_input


if __name__ == "__main__":
    typer.run(Day11().run)

# vim:expandtab:sw=4:ts=4
