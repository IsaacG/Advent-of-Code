#!/bin/python
"""Advent of Code, Day 1: Inverse Captcha."""

from collections.abc import Callable
from lib import aoc

SAMPLE = (
    [
        ("1122", 3),
        ("1111", 4),
        ("1234", 0),
        ("91212129", 9),
    ],
    [
        ("1212", 6),
        ("1221", 0),
        ("123425", 4),
        ("123123", 12),
        ("12131415", 4),
    ]
)


class Day01(aoc.Challenge):
    """Day 1: Inverse Captcha."""

    TESTS = [
        aoc.TestCase(inputs=data[0], part=part, want=data[1])
        for part, dataset in enumerate(SAMPLE, 1)
        for data in dataset
    ]
    INPUT_PARSER = aoc.parse_one_str

    def solver(self, parsed_input: str, part_one: bool) -> int:
        """Sum all digits which match the corresponding digit."""
        # Part one: compare digits to subsequent digit.
        # Part two: compare digits to digits halfway around the list.
        offset = 1 if part_one else len(parsed_input) // 2
        shifted_list = parsed_input[offset:] + parsed_input[:offset]
        return sum(
            int(digit)
            for digit, corresponding in zip(parsed_input, shifted_list)
            if digit == corresponding
        )

# vim:expandtab:sw=4:ts=4
