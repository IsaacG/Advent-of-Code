#!/bin/python
"""Advent of Code, Day 1: Inverse Captcha."""

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
    # PARAMETERIZED_INPUTS = [False, True]

    def part1(self, parsed_input: str) -> int:
        """Sum all numbers which match the subsequent number."""
        return sum(
            int(a)
            for a, b in zip(parsed_input, parsed_input[1:] + parsed_input[:1])
            if a == b
        )

    def part2(self, parsed_input: str) -> int:
        """Sum all numbers which match the subsequent number."""
        offset = len(parsed_input) // 2
        return sum(
            int(a)
            for a, b in zip(parsed_input, parsed_input[offset:] + parsed_input[:offset])
            if a == b
        )

# vim:expandtab:sw=4:ts=4
